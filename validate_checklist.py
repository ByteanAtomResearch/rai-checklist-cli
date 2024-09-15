import yaml
import sys
import argparse

def load_config(config_file):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def validate_checklist(checklist_file, project_type, config):
    with open(checklist_file, 'r') as f:
        checklist = yaml.safe_load(f)

    required_sections = config.get(project_type, config['default'])['required_sections']
    missing_sections = [s for s in required_sections if s not in checklist]

    if missing_sections:
        print(f'Missing required sections for {project_type}: {missing_sections}')
        return False
    print(f'All required sections for {project_type} are present.')
    return True

def main():
    parser = argparse.ArgumentParser(description='Validate checklist based on project type.')
    parser.add_argument('checklist_file', help='Path to the checklist YAML file')
    parser.add_argument('--project-type', default='default', help='Project type (default, machine_learning, web_application, etc.)')
    parser.add_argument('--config', default='checklist_config.yaml', help='Path to the configuration file')
    args = parser.parse_args()

    config = load_config(args.config)
    if validate_checklist(args.checklist_file, args.project_type, config):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()