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

def main():
    template_manager = TemplateManager(Path(__file__).parent / 'templates.yaml')
    
    parser = argparse.ArgumentParser(
        description='Responsible AI Checklist CLI for LLM Projects',
        epilog='Examples:\n'
               '  Generate a checklist:\n'
               '    %(prog)s generate -t default -o checklist.md\n'
               '  Create a custom template:\n'
               '    %(prog)s create-template',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Generate checklist command
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

    # Create custom template command
    create_parser = subparsers.add_parser('create-template', 
        help='Create a custom checklist template',
        description='Interactively create a custom checklist template and save it for future use'
    )

    args = parser.parse_args()

    if args.command == 'create-template':
        create_custom_template(template_manager)
    elif args.command == 'generate':
        if not args.output.endswith(f".{args.format}"):
            args.output += f".{args.format}"
        
        template = template_manager.get_template(args.template)
        
        if args.sections is None:
            args.sections = list(template.keys())
        
        try:
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
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
