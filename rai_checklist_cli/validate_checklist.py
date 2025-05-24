import yaml
import sys
import argparse

def load_config(config_file):
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def validate_checklist(checklist_file, project_type, config):
    with open(checklist_file, 'r') as f:
        checklist = yaml.safe_load(f)

    required_sections = config.get(project_type, {}).get('required_sections', config.get('default', {}).get('required_sections', []))
    missing_sections = [s for s in required_sections if s not in checklist]
    validation_messages = []
    is_valid = True

    critical_project_types = config.get('critical_project_types', [])
    critical_sections = config.get('critical_sections', [])
    missing_critical_sections = []

    is_critical_project = project_type in critical_project_types

    if missing_sections:
        validation_messages.append(f'Missing required sections for {project_type}: {missing_sections}')
        is_valid = False

    if is_critical_project:
        validation_messages.append(f'Project type "{project_type}" is critical. Validating critical sections.')
        missing_critical_sections = [s for s in critical_sections if s not in checklist]
        if missing_critical_sections:
            validation_messages.append(f'Missing critical sections for {project_type}: {missing_critical_sections}')
            is_valid = False

    if is_valid:
        if is_critical_project:
            validation_messages.append(f'All required and critical sections for {project_type} are present.')
        else:
            validation_messages.append(f'All required sections for {project_type} are present.')
    
    return is_valid, validation_messages

def main():
    parser = argparse.ArgumentParser(description='Validate checklist based on project type.')
    parser.add_argument('checklist_file', help='Path to the checklist YAML file')
    parser.add_argument('--project-type', default='default', help='Project type (default, machine_learning, web_application, etc.)')
    parser.add_argument('--config', default='checklist_config.yaml', help='Path to the configuration file')
    args = parser.parse_args()

    config = load_config(args.config)
    is_valid, messages = validate_checklist(args.checklist_file, args.project_type, config)
    
    for message in messages:
        print(message)
        
    if is_valid:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()