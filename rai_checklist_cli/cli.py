import argparse
import sys
import logging
from pathlib import Path

from rai_checklist_cli.template_manager import TemplateManager
from rai_checklist_cli.checklist_generator import generate_checklist
from rai_checklist_cli.template_utils import create_custom_template, display_available_templates, focus_on_section
from rai_checklist_cli.config import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main(args=None):
    parser = argparse.ArgumentParser(
        description='Responsible AI Checklist CLI for LLM Projects',
        epilog='Examples:\n'
               '  Generate a checklist:\n'
               '    %(prog)s generate -t default -o checklist.md\n'
               '  Create a custom template:\n'
               '    %(prog)s create-template',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--template-file', help='Path to a custom template file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    generate_parser = subparsers.add_parser('generate', 
        help='Generate a responsible AI checklist',
        description='Generate a customizable responsible AI checklist for LLM projects'
    )
    
    output_group = generate_parser.add_argument_group('Output options')
    output_group.add_argument(
        '-o', '--output',
        default='responsible_ai_checklist_llm.md',
        help='The output file name (default: %(default)s)'
    )
    output_group.add_argument(
        '-f', '--format',
        choices=['md', 'yaml', 'json'],
        default='md',
        help='Specify the output format (default: %(default)s)'
    )
    
    template_group = generate_parser.add_argument_group('Template options')
    template_group.add_argument(
        '-t', '--template',
        help='Specify which template to use (default: %(default)s)'
    )
    template_group.add_argument(
        '-s', '--sections',
        nargs='+',
        metavar='SECTION',
        help='Specify which sections to include (default: all sections in the template)'
    )

    create_parser = subparsers.add_parser('create-template', 
        help='Create a custom checklist template',
        description='Interactively create a custom checklist template and save it for future use'
    )

    list_parser = subparsers.add_parser('list-templates', 
        help='List all available templates and sections',
        description='List the available templates and their respective sections'
    )

    focus_parser = subparsers.add_parser('focus', 
        help='Focus on a specific section in a template',
        description='Focus on and display a specific section from a selected template'
    )
    focus_parser.add_argument(
        '-t', '--template',
        help='Specify the template to use (default: %(default)s)'
    )
    focus_parser.add_argument(
        '-s', '--section',
        required=True,
        help='Specify the section to focus on'
    )

    parsed_args = parser.parse_args(args)

    if parsed_args.verbose:
        logger.setLevel(logging.DEBUG)

    try:
        template_manager = TemplateManager(parsed_args.template_file) if parsed_args.template_file else TemplateManager()
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

    if parsed_args.command == 'create-template':
        create_custom_template(template_manager)
    elif parsed_args.command == 'generate':
        generate_command(parsed_args, template_manager)
    elif parsed_args.command == 'list-templates':
        display_available_templates(template_manager.templates)
    elif parsed_args.command == 'focus':
        focus_on_section(template_manager.templates, parsed_args.template, parsed_args.section)
    else:
        parser.print_help()

def generate_command(args, template_manager):
    if not args.output.endswith(f".{args.format}"):
        args.output += f".{args.format}"
    
    template = template_manager.get_template(args.template)
    
    if args.sections is None:
        args.sections = list(template.keys())
    
    try:
        checklist_content = generate_checklist(template, args.sections, args.format)
        with open(args.output, 'w') as f:
            f.write(checklist_content)
        logger.info(f'Responsible AI checklist for LLM projects generated and saved to {args.output}')
    except (IOError, ValueError) as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")
        sys.exit(1)

if __name__ == '__main__':
    main()
