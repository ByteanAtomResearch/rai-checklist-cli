import sys
import os
import unittest
from unittest.mock import patch
from io import StringIO
import subprocess
import pytest
from rai_checklist_cli.cli import main, generate_checklist

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestCLI(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_help_command(self, mock_stdout):
        with self.assertRaises(SystemExit):
            main(['--help'])
        self.assertIn('usage:', mock_stdout.getvalue())

    @patch('rai_checklist_cli.cli.TemplateManager')
    def test_generate_checklist(self, mock_template_manager):
        mock_template = {
            'name': 'Default Template',
            'section1': {'title': 'Section 1', 'items': ['Item 1', 'Item 2']},
            'section2': {'title': 'Section 2', 'items': ['Item 3', 'Item 4']}
        }
        mock_template_manager.return_value.get_template.return_value = mock_template
        
        result = generate_checklist(mock_template, ['section1', 'section2'], 'md')
        
        self.assertIn("# Responsible AI Checklist for LLM Projects - Default Template", result)
        self.assertIn("## Section 1", result)
        self.assertIn("- [ ] Item 1", result)
        self.assertIn("## Section 2", result)
        self.assertIn("- [ ] Item 4", result)

    # Add more tests as needed

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    print(f"Command: {' '.join(command)}")
    print(f"Exit code: {result.returncode}")
    print(f"Output:\n{result.stdout}")
    print(f"Error:\n{result.stderr}")
    print("-" * 50)
    return result

def test_cli():
    commands = [
        ["rai-checklist", "generate", "-o", "test_output.md", "-f", "md"],
        ["rai-checklist", "generate", "-o", "test_output.yaml", "-f", "yaml"],
        ["rai-checklist", "list-templates"],
        ["rai-checklist", "focus", "-t", "default", "-s", "data_collection"],
    ]

    for command in commands:
        result = run_command(command)
        assert result.returncode == 0, f"Command failed: {' '.join(command)}"

def test_generate_checklist_with_custom_title(capsys):
    with pytest.raises(SystemExit) as e:
        main(['generate', '-t', 'default', '-o', 'test_checklist.md', '--title', 'Custom Checklist Title'])
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert 'Responsible AI checklist for LLM projects generated and saved to test_checklist.md' in captured.out

def test_generate_checklist_without_title(capsys):
    # Ensure the output file does not exist before running the test
    output_file = 'test_checklist.md'
    if os.path.exists(output_file):
        os.remove(output_file)

    with pytest.raises(SystemExit) as e:
        main(['generate', '-t', 'default', '-o', output_file])
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert 'Responsible AI checklist for LLM projects generated and saved to test_checklist.md' in captured.out

def test_generate_checklist_with_invalid_arguments(capsys):
    with pytest.raises(SystemExit) as e:
        main(['generate', '-t', 'invalid_template', '-o', 'test_checklist.md'])
    assert e.value.code == 1  # Ensure the exit code is 1 for invalid arguments
