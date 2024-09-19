import argparse
import sys
import logging
from pathlib import Path

from rai_checklist_cli.template_manager import TemplateManager
from rai_checklist_cli.checklist_generator import generate_checklist
from rai_checklist_cli.template_utils import create_custom_template, display_available_templates, focus_on_section
from rai_checklist_cli.config import load_config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description='Responsible AI Checklist CLI for LLM Projects',
        epilog='Examples:\n'
               '  Generate a checklist:\n'
               '    %(prog)s generate -o checklist.md -f md\n'
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
    generate_parser.add_argument('-o', '--output', default='responsible_ai_checklist_llm.md', help='The output file name (default: %(default)s)')
    generate_parser.add_argument('-f', '--format', choices=['md', 'yaml'], default='md', help='Specify the output format (default: %(default)s)')
    generate_parser.add_argument('-t', '--template', help='Specify which template to use (default: %(default)s)', default='default')
    generate_parser.add_argument('-s', '--sections', nargs='+', metavar='SECTION', help='Specify which sections to include (default: all sections in the template)')
    generate_parser.add_argument('-w', '--overwrite', action='store_true', help='Overwrite existing output file')
    generate_parser.add_argument('-l', '--checklist', help='Specify a custom checklist file to use')
    generate_parser.add_argument('--title', default="Responsible AI Checklist for ML & AI Projects", help='Specify a custom title for the checklist')
    generate_parser.add_argument('--project-type', help='Specify the project type for validation (e.g., machine_learning, web_application)')
    generate_parser.add_argument('--config', help='Path to the configuration file for validation')

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
    focus_parser.add_argument('-t', '--template', help='Specify the template to use (default: %(default)s)')
    focus_parser.add_argument('-s', '--section', required=True, help='Specify the section to focus on')

    list_sections_parser = subparsers.add_parser('list-sections', 
        help='List all available sections in a template',
        description='List the available sections in a specified template'
    )
    list_sections_parser.add_argument('-t', '--template', required=True, help='Specify the template to list sections from')

    parsed_args = parser.parse_args(args)

    if parsed_args.verbose:
        logger.setLevel(logging.DEBUG)

    try:
        template_manager = TemplateManager(parsed_args.template_file)
    except FileNotFoundError as e:
        logger.error(f"Error loading templates: {e}")
        logger.debug("Make sure the templates.yaml file is present in the package or provide a valid custom template file.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error loading templates: {e}")
        logger.debug("", exc_info=True)
        sys.exit(1)

    if parsed_args.command == 'create-template':
        create_custom_template(template_manager)
    elif parsed_args.command == 'list-templates':
        display_available_templates(template_manager.templates)
    elif parsed_args.command == 'focus':
        focus_on_section(template_manager.templates, parsed_args.template, parsed_args.section)
    elif parsed_args.command == 'list-sections':
        template = template_manager.get_template(parsed_args.template)
        sections = template_manager.get_available_sections(template)
        if sections:
            print("Available sections:")
            for section in sections:
                print(f"  - {section}")
        else:
            logger.error(f"No sections found in template {parsed_args.template}")
    elif parsed_args.command == 'generate':
        template = template_manager.get_template(parsed_args.template)
        sections = parsed_args.sections or list(template.keys())
        
        # Verify sections
        available_sections = template_manager.get_available_sections(template)
        invalid_sections = [section for section in sections if section not in available_sections]
        if invalid_sections:
            logger.error(f"Invalid sections specified: {', '.join(invalid_sections)}")
            sys.exit(1)
        
        try:
            checklist = generate_checklist(
                template,
                sections,
                parsed_args.format,
                title=parsed_args.title
            )
        except AttributeError as e:
            logger.error(f"Error generating checklist: {e}")
            logger.debug("Make sure all required arguments are provided.")
            sys.exit(1)
        
        if not parsed_args.output.endswith(f".{parsed_args.format}"):
            parsed_args.output += f".{parsed_args.format}"
        
        if Path(parsed_args.output).exists() and not parsed_args.overwrite:
            logger.error(f"Output file {parsed_args.output} already exists. Use -w or --overwrite to overwrite.")
            sys.exit(1)

        with open(parsed_args.output, 'w') as f:
            f.write(checklist)
        logger.info(f'Responsible AI checklist for LLM projects generated and saved to {parsed_args.output}')
    elif parsed_args.command is None:
        generate_command(parsed_args, template_manager)
    else:
        parser.print_help()
        sys.exit(1)

def generate_command(args, template_manager):
    if not args.output.endswith(f".{args.format}"):
        args.output += f".{args.format}"
    
    if Path(args.output).exists() and not args.overwrite:
        logger.error(f"Output file {args.output} already exists. Use -w or --overwrite to overwrite.")
        sys.exit(1)

    config = load_config(args.config) if args.config else None
    
    try:
        template = template_manager.get_template(args.template)
        logger.debug(f"Retrieved template: {args.template}")
        
        if args.sections is None:
            args.sections = list(template.keys())
        logger.debug(f"Sections to include: {args.sections}")
        
        checklist_content = generate_checklist(
            template, 
            args.sections, 
            args.format, 
            args.project_type,
            config,
            custom_checklist=args.checklist
        )
        logger.debug("Checklist content generated successfully")
        
        with open(args.output, 'w') as f:
            f.write(checklist_content)
        logger.info(f'Responsible AI checklist for LLM projects generated and saved to {args.output}')
    except KeyError as e:
        logger.error(f"Error: Missing key in template - {e}")
        logger.debug("Template structure:", exc_info=True)
        sys.exit(1)
    except AttributeError as e:
        logger.error(f"Error: Missing attribute - {e}")
        logger.debug("Ensure all required fields are present in the template", exc_info=True)
        sys.exit(1)
    except (IOError, ValueError) as e:
        logger.error(f"Error: {e}")
        logger.debug("", exc_info=True)
        sys.exit(1)
    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")
        logger.debug("", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
    sys.exit(0)
