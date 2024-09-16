import argparse
import sys
import json
import yaml
from pathlib import Path

class TemplateManager:
    def __init__(self, template_file):
        self.template_file = template_file
        self.templates = self.load_templates()

    def load_templates(self):
        with open(self.template_file, 'r') as f:
            return yaml.safe_load(f)

    def get_template(self, template_name):
        return self.templates.get(template_name, self.templates['default'])

    def get_available_templates(self):
        return list(self.templates.keys())

    def save_template(self, template_name, template_data):
        self.templates[template_name] = template_data
        with open(self.template_file, 'w') as f:
            yaml.dump(self.templates, f)
        print(f"Template '{template_name}' has been saved successfully.")

def generate_section(section_data):
    section = f"## {section_data['title']}\n"
    for item in section_data['items']:
        section += f"- [ ] {item}\n"
    return section + "\n"

def generate_checklist(template, sections, file_format):
    if file_format not in ["md", "yaml", "json"]:
        raise ValueError(f"Unsupported file format: {file_format}")
    
    if file_format == "md":
        checklist = f"# Responsible AI Checklist for LLM Projects - {template['name']}\n\n"
        for section in sections:
            if section in template:
                checklist += generate_section(template[section])
            else:
                print(f"Warning: Section '{section}' is not in the template and will be skipped.", file=sys.stderr)
        return checklist

    # Build a dictionary representation of the checklist
    checklist_dict = {}
    for section in sections:
        if section in template:
            checklist_dict[template[section]['title']] = template[section]['items']
        else:
            print(f"Warning: Section '{section}' is not in the template and will be skipped.", file=sys.stderr)
    
    if file_format == "yaml":
        return yaml.dump(checklist_dict, sort_keys=False)
    elif file_format == "json":
        return json.dumps(checklist_dict, indent=2)

def create_custom_template(template_manager):
    template_name = input("Enter a name for your custom template: ").strip()
    if template_name in template_manager.get_available_templates():
        overwrite = input(f"Template '{template_name}' already exists. Do you want to overwrite it? (y/n): ").lower()
        if overwrite != 'y':
            print("Template creation cancelled.")
            return

    template_data = {}
    while True:
        section_name = input("Enter a section name (or press Enter to finish): ").strip()
        if not section_name:
            break

        section_title = input(f"Enter the title for '{section_name}': ").strip()
        items = []
        print(f"Enter items for '{section_name}' (one per line, press Enter twice to finish):")
        while True:
            item = input().strip()
            if not item:
                break
            items.append(item)

        template_data[section_name] = {
            'title': section_title,
            'items': items
        }

    template_manager.save_template(template_name, template_data)

# Fuunction to load templates from templates.yaml
def load_templates(template_file='templates.yaml'):
    with open(template_file, 'r') as f:
        templates = yaml.safe_load(f)
    return templates

# function to list templates and sections
def display_available_templates(templates):
    print("Available Templates and Sections:")
    for template_name, sections in templates.items():
        print(f"Template: {template_name}")
        for section_name, section_content in sections.items():
            print(f"  - Section: {section_content['title']}")

# focus on sepcific section
def focus_on_section(templates, selected_template, selected_section):
    if selected_template not in templates:
        print(f"Template '{selected_template}' not found.")
        return

    template = templates[selected_template]
    if selected_section not in template:
        print(f"Section '{selected_section}' not found in template '{selected_template}'.")
        return

    section = template[selected_section]
    print(f"Focused Section: {section['title']}")
    for item in section['items']:
        print(f"- {item}")

def main():
    # Initialize the TemplateManager to manage templates
    template_manager = TemplateManager(Path(__file__).parent / 'templates.yaml')
    
    # Setup ArgumentParser for CLI
    parser = argparse.ArgumentParser(
        description='Responsible AI Checklist CLI for LLM Projects',
        epilog='Examples:\n'
               '  Generate a checklist:\n'
               '    %(prog)s generate -t default -o checklist.md\n'
               '  Create a custom template:\n'
               '    %(prog)s create-template',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create subparsers for various commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Subcommand to generate checklists
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
        choices=template_manager.get_available_templates(),
        default='default',
        help='Specify which template to use (default: %(default)s)'
    )
    template_group.add_argument(
        '-s', '--sections',
        nargs='+',
        metavar='SECTION',
        help='Specify which sections to include (default: all sections in the template)'
    )

    # Subcommand to create a custom template
    create_parser = subparsers.add_parser('create-template', 
        help='Create a custom checklist template',
        description='Interactively create a custom checklist template and save it for future use'
    )

    # Subcommand to list all available templates and sections
    list_parser = subparsers.add_parser('list-templates', 
        help='List all available templates and sections',
        description='List the available templates and their respective sections'
    )

    # Subcommand to focus on a specific section in a template
    focus_parser = subparsers.add_parser('focus', 
        help='Focus on a specific section in a template',
        description='Focus on and display a specific section from a selected template'
    )
    focus_parser.add_argument(
        '-t', '--template',
        choices=template_manager.get_available_templates(),
        default='default',
        help='Specify the template to use (default: %(default)s)'
    )
    focus_parser.add_argument(
        '-s', '--section',
        required=True,
        help='Specify the section to focus on'
    )

    # Parse the arguments provided by the user
    args = parser.parse_args()

    # Handle the create-template command
    if args.command == 'create-template':
        create_custom_template(template_manager)

    # Handle the generate command
    elif args.command == 'generate':
        if not args.output.endswith(f".{args.format}"):
            args.output += f".{args.format}"
        
        # Get the selected template
        template = template_manager.get_template(args.template)
        
        # If no sections are specified, include all sections
        if args.sections is None:
            args.sections = list(template.keys())
        
        try:
            # Generate the checklist based on the template and format
            checklist_content = generate_checklist(template, args.sections, args.format)
            with open(args.output, 'w') as f:
                f.write(checklist_content)
            print(f'Responsible AI checklist for LLM projects generated and saved to {args.output}')
        except IOError as e:
            print(f"Error writing to file {args.output}: {e}", file=sys.stderr)
            sys.exit(1)
        except ValueError as ve:
            print(f"Error: {ve}", file=sys.stderr)
            sys.exit(1)
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}", file=sys.stderr)
            sys.exit(1)

    # Handle the list-templates command
    elif args.command == 'list-templates':
        templates = template_manager.templates
        display_available_templates(templates)

    # Handle the focus command
    elif args.command == 'focus':
        templates = template_manager.templates
        focus_on_section(templates, args.template, args.section)

    # If no valid command is provided, print the help message
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
