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
        ["rai-checklist", "-o", "test_output.md"],
        ["rai-checklist", "-o", "test_output.yaml", "-f", "yaml"],
        ["rai-checklist", "-o", "test_output.json", "-f", "json"],
        ["rai-checklist", "generate", "-o", "test_generate.md"],
        ["rai-checklist", "list-templates"],
        ["rai-checklist", "focus", "-t", "default", "-s", "data_collection"],
    ]

    for command in commands:
        result = run_command(command)
        assert result.returncode == 0, f"Command failed: {' '.join(command)}"

    # Check if output files were created
    for file in ["test_output.md", "test_output.yaml", "test_output.json", "test_generate.md"]:
        assert os.path.exists(file), f"Output file not created: {file}"
        os.remove(file)

if __name__ == '__main__':
    unittest.main()

def test_generate_checklist_with_custom_title(capsys):
    with pytest.raises(SystemExit) as e:
        main(['generate', '-t', 'default', '-o', 'test_checklist.md', '--title', 'Custom Checklist Title'])
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert 'Responsible AI checklist for LLM projects generated and saved to test_checklist.md' in captured.out

def test_generate_checklist_without_title(capsys):
    with pytest.raises(SystemExit) as e:
        main(['generate', '-t', 'default', '-o', 'test_checklist.md'])
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert 'Responsible AI checklist for LLM projects generated and saved to test_checklist.md' in captured.out

def test_generate_checklist_with_invalid_arguments(capsys):
    with pytest.raises(SystemExit) as e:
        main(['generate', '-t', 'non_existent_template'])
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert 'Error generating checklist' in captured.err