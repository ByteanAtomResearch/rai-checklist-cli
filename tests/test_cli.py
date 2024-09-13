import unittest
import os
from unittest.mock import patch
from rai_checklist_cli.cli import generate_checklist

class TestCLI(unittest.TestCase):

    def test_generate_checklist_all_sections(self):
        sections = list(generate_checklist.SECTION_FUNCTIONS.keys())
        checklist = generate_checklist(sections)
        self.assertIn("## Ethics and Compliance", checklist)
        self.assertIn("## Data Privacy and Security", checklist)
        # Add assertions for other sections

    def test_generate_checklist_specific_sections(self):
        sections = ['ethics', 'fairness']
        checklist = generate_checklist(sections)
        self.assertIn("## Ethics and Compliance", checklist)
        self.assertIn("## Bias and Fairness", checklist)
        self.assertNotIn("## Data Privacy and Security", checklist)

    @patch('builtins.open')
    def test_file_creation(self, mock_open):
        from rai_checklist_cli.cli import main
        test_args = ['rai-checklist', '-o', 'test_checklist.md', '-s', 'ethics', 'privacy']
        with patch('sys.argv', test_args):
            main()
            mock_open.assert_called_with('test_checklist.md', 'w')

    def test_invalid_section(self):
        sections = ['invalid_section']
        with patch('sys.stderr') as mock_stderr:
            checklist = generate_checklist(sections)
            mock_stderr.write.assert_called_with("Warning: Section 'invalid_section' is not recognized and will be skipped.\n")
            self.assertEqual(checklist, "# Responsible AI Checklist\n\n")

if __name__ == '__main__':
    unittest.main()