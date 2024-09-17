import sys
import os
import unittest
from unittest.mock import patch
from io import StringIO
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rai_checklist_cli.cli import main, generate_checklist

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

if __name__ == '__main__':
    unittest.main()