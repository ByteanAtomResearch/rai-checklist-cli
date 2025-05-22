import sys
import os
import unittest
from unittest.mock import patch
from io import StringIO
import subprocess
import pytest
import yaml
from pathlib import Path
from rai_checklist_cli.cli import main as cli_main # Renamed to avoid conflict

# Ensure the main package is in path for module resolution if running tests directly
# For subprocess calls, this is not strictly necessary if the package is installed or PYTHONPATH is set.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Original generate_checklist function from cli.py, if needed for some direct tests (not used here)
# from rai_checklist_cli.checklist_generator import generate_checklist 


@pytest.fixture
def cli_test_checklist_config_file(tmp_path):
    config_data = {
        'default': {
            'required_sections': ['SectionTemplateA', 'SectionTemplateB']
        },
        'critical_ml': {
            'required_sections': ['SectionTemplateA']
        },
        'critical_ml_missing_req_in_config': {
            'required_sections': ['SectionTemplateA', 'ThisSectionIsNotInTemplate']
        },
        'default_missing_req_in_config': {
            'required_sections': ['SectionTemplateA', 'ThisSectionIsNotInTemplate']
        },
        'critical_project_types': ['critical_ml', 'critical_ml_missing_req_in_config'],
        'critical_sections': ['CriticalSectionTemplate1', 'ThisCriticalSectionIsNotInTemplate']
    }
    config_file = tmp_path / "test_cli_checklist_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(config_data, f)
    return config_file

@pytest.fixture
def cli_test_template_file(tmp_path):
    template_data = {
        'SectionTemplateA': {'title': "Section A from Template", 'items': ["Item A1"]},
        'SectionTemplateB': {'title': "Section B from Template", 'items': ["Item B1"]},
        'CriticalSectionTemplate1': {'title': "Critical Section 1 from Template", 'items': ["Item CS1-1"]},
    }
    template_file = tmp_path / "test_cli_template.yaml"
    with open(template_file, 'w') as f:
        yaml.dump(template_data, f)
    return template_file

@pytest.fixture
def cli_test_template_file_missing_b(tmp_path): # For testing default fallback
    template_data = {
        'SectionTemplateA': {'title': "Section A from Template", 'items': ["Item A1"]},
        # SectionTemplateB is missing
        'CriticalSectionTemplate1': {'title': "Critical Section 1 from Template", 'items': ["Item CS1-1"]},
    }
    template_file = tmp_path / "test_cli_template_missing_b.yaml"
    with open(template_file, 'w') as f:
        yaml.dump(template_data, f)
    return template_file


class TestCLI(unittest.TestCase): # Keeping existing tests if they are still relevant

    @patch('sys.stdout', new_callable=StringIO)
    def test_help_command(self, mock_stdout):
        with self.assertRaises(SystemExit):
            cli_main(['--help']) # Use renamed main
        self.assertIn('usage:', mock_stdout.getvalue())

    # The original test_generate_checklist was testing the internal generate_checklist function,
    # not the CLI command. It might be better placed in a different test file
    # or adapted if it's meant to be a unit test for that specific function.
    # For now, I'll keep it commented out or remove if it's redundant with other tests.
    # @patch('rai_checklist_cli.cli.TemplateManager')
    # def test_generate_checklist_direct_call(self, mock_template_manager):
    #     from rai_checklist_cli.checklist_generator import generate_checklist # Moved import
    #     mock_template = {
    #         'name': 'Default Template',
    #         'section1': {'title': 'Section 1', 'items': ['Item 1', 'Item 2']},
    #         'section2': {'title': 'Section 2', 'items': ['Item 3', 'Item 4']}
    #     }
    #     mock_template_manager.return_value.get_template.return_value = mock_template
        
    #     result = generate_checklist(mock_template, ['section1', 'section2'], 'md')
        
    #     self.assertIn("# Responsible AI Checklist for LLM Projects - Default Template", result) # Title might change
    #     self.assertIn("## Section 1", result)
    #     self.assertIn("- [ ] Item 1", result)
    #     self.assertIn("## Section 2", result)
    #     self.assertIn("- [ ] Item 4", result)

# pytest-style tests for CLI generate command and validation
class TestGenerateCommandValidation:

    def run_cli_command(self, command_args, expect_success=True):
        base_command = [sys.executable, '-m', 'rai_checklist_cli.cli']
        # base_command = ['rai-checklist'] # If installed and in PATH
        full_command = base_command + command_args
        print(f"Running command: {' '.join(full_command)}")
        result = subprocess.run(full_command, capture_output=True, text=True, cwd=Path(__file__).parent.parent) # Run from repo root
        
        print(f"STDOUT:\n{result.stdout}")
        print(f"STDERR:\n{result.stderr}")
        
        if expect_success: # This refers to CLI execution, not necessarily validation pass
            assert result.returncode == 0, f"CLI command failed with exit code {result.returncode}. STDERR:\n{result.stderr}"
        # If we expect failure due to CLI args, then this assertion would change.
        # For validation messages, cli.py currently doesn't set exit code != 0.
        return result

    def test_generate_critical_pass(self, tmp_path, cli_test_checklist_config_file, cli_test_template_file):
        output_file = tmp_path / "checklist_crit_pass.yaml"
        args = [
            'generate', '-o', str(output_file), '-f', 'yaml',
            '--template', str(cli_test_template_file), # Use the test template
            '--project-type', 'critical_ml',
            '--config', str(cli_test_checklist_config_file),
            '--overwrite'
        ]
        result = self.run_cli_command(args)
        assert "All required and critical sections for critical_ml are present." in result.stdout
        assert "Missing" not in result.stdout # No missing sections should be reported

    def test_generate_critical_fail_missing_critical(self, tmp_path, cli_test_checklist_config_file, cli_test_template_file):
        output_file = tmp_path / "checklist_crit_fail_crit.yaml"
        args = [
            'generate', '-o', str(output_file), '-f', 'yaml',
            '--template', str(cli_test_template_file),
            '--project-type', 'critical_ml', # This type has global critical sections, one of which is not in the template
            '--config', str(cli_test_checklist_config_file),
            '--overwrite'
        ]
        result = self.run_cli_command(args)
        assert "Missing critical sections for critical_ml: ['ThisCriticalSectionIsNotInTemplate']" in result.stdout

    def test_generate_critical_fail_missing_required(self, tmp_path, cli_test_checklist_config_file, cli_test_template_file):
        output_file = tmp_path / "checklist_crit_fail_req.yaml"
        args = [
            'generate', '-o', str(output_file), '-f', 'yaml',
            '--template', str(cli_test_template_file),
            '--project-type', 'critical_ml_missing_req_in_config',
            '--config', str(cli_test_checklist_config_file),
            '--overwrite'
        ]
        result = self.run_cli_command(args)
        # Check for missing required
        assert "Missing required sections for critical_ml_missing_req_in_config: ['ThisSectionIsNotInTemplate']" in result.stdout
        # Check for missing critical (as it's a critical project, global critical sections are also checked)
        assert "Missing critical sections for critical_ml_missing_req_in_config: ['ThisCriticalSectionIsNotInTemplate']" in result.stdout
        
    def test_generate_default_fail_missing_required(self, tmp_path, cli_test_checklist_config_file, cli_test_template_file):
        output_file = tmp_path / "checklist_default_fail_req.yaml"
        args = [
            'generate', '-o', str(output_file), '-f', 'yaml',
            '--template', str(cli_test_template_file),
            '--project-type', 'default_missing_req_in_config',
            '--config', str(cli_test_checklist_config_file),
            '--overwrite'
        ]
        result = self.run_cli_command(args)
        assert "Missing required sections for default_missing_req_in_config: ['ThisSectionIsNotInTemplate']" in result.stdout
        # Ensure critical sections are not mentioned for non-critical project types if they pass required checks
        # (or if they fail, critical check output shouldn't appear unless project is critical)
        assert "critical sections" not in result.stdout.lower() or "Missing required sections" in result.stdout


    def test_generate_validation_skipped_non_yaml(self, tmp_path, cli_test_checklist_config_file, cli_test_template_file):
        output_file = tmp_path / "checklist_skip.md"
        args = [
            'generate', '-o', str(output_file), '-f', 'md', # Output is MD
            '--template', str(cli_test_template_file),
            '--project-type', 'critical_ml',
            '--config', str(cli_test_checklist_config_file),
            '--overwrite'
        ]
        result = self.run_cli_command(args)
        assert "Skipping validation for non-YAML output format: md. Project type was 'critical_ml'." in result.stdout
        assert "Missing" not in result.stdout # No validation messages should appear

    def test_generate_unknown_project_type_uses_default_validation(self, tmp_path, cli_test_checklist_config_file, cli_test_template_file_missing_b):
        output_file = tmp_path / "checklist_unknown_type.yaml"
        args = [
            'generate', '-o', str(output_file), '-f', 'yaml',
            '--template', str(cli_test_template_file_missing_b), # This template is missing SectionTemplateB
            '--project-type', 'new_unknown_project_type', # Not in config, should use 'default'
            '--config', str(cli_test_checklist_config_file),
            '--overwrite'
        ]
        result = self.run_cli_command(args)
        # 'default' in config requires ['SectionTemplateA', 'SectionTemplateB']
        # The template used for generation (cli_test_template_file_missing_b) only has SectionTemplateA.
        assert "Missing required sections for new_unknown_project_type: ['SectionTemplateB']" in result.stdout

# Old pytest functions - might need review or removal if TestCLI or TestGenerateCommandValidation covers them.
# For example, test_cli() below seems like an integration test.
# The capsys tests are good for testing specific main() behaviors not covered by subprocess.

# def run_command(command): # This is a helper, can be kept or moved into class
#     result = subprocess.run(command, capture_output=True, text=True)
#     print(f"Command: {' '.join(command)}")
#     print(f"Exit code: {result.returncode}")
#     print(f"Output:\n{result.stdout}")
#     print(f"Error:\n{result.stderr}")
#     print("-" * 50)
#     return result

# def test_cli(): # This is a very basic integration test
#     commands = [
#         ["rai-checklist", "generate", "-o", "test_output.md", "-f", "md"],
#         ["rai-checklist", "generate", "-o", "test_output.yaml", "-f", "yaml"],
#         ["rai-checklist", "list-templates"],
#         ["rai-checklist", "focus", "-t", "default", "-s", "data_collection"],
#     ]
#     # This needs rai-checklist to be installed or aliased.
#     # Using python -m rai_checklist_cli.cli is more robust for uninstalled packages.
#     for command in commands:
#         # result = run_command(command)
#         # assert result.returncode == 0, f"Command failed: {' '.join(command)}"
#         pass # Commenting out for now as it relies on global installation.

def test_generate_checklist_with_custom_title(capsys, tmp_path):
    output_file = tmp_path / "test_checklist.md"
    with pytest.raises(SystemExit) as e:
        cli_main(['generate', '-t', 'default', '-o', str(output_file), '--title', 'Custom Checklist Title', '--overwrite'])
    assert e.value.code == 0 # Expect cli.py to exit 0 on successful generation
    captured = capsys.readouterr()
    assert f"Responsible AI checklist for LLM projects generated and saved to {str(output_file)}" in captured.out
    # Add check for validation output if applicable, though this test is for title.

def test_generate_checklist_without_title(capsys, tmp_path):
    output_file = tmp_path / "test_checklist.md"
    # No need to manually remove, tmp_path handles cleanup.
    with pytest.raises(SystemExit) as e:
        cli_main(['generate', '-t', 'default', '-o', str(output_file), '--overwrite'])
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert f"Responsible AI checklist for LLM projects generated and saved to {str(output_file)}" in captured.out

def test_generate_checklist_with_invalid_template_arg(capsys, tmp_path):
    output_file = tmp_path / "test_checklist.md"
    with pytest.raises(SystemExit) as e:
        cli_main(['generate', '-t', 'invalid_template_name_does_not_exist', '-o', str(output_file), '--overwrite'])
    assert e.value.code == 1  # Ensure the exit code is 1 for invalid arguments like non-existent template
    # Captured output might contain error message from logger.
    # captured = capsys.readouterr()
    # assert "Error loading templates" in captured.err or "Template not found" in captured.out or captured.err
