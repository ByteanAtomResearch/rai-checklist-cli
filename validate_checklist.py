import yaml
import sys

with open('examples/checklist.yaml') as f:
    checklist = yaml.safe_load(f)
    required_sections = ['Ethical considerations', 'Deployment Monitoring']
    missing_sections = [s for s in required_sections if s not in checklist]
    if missing_sections:
        print(f'Missing required sections: {missing_sections}')
        sys.exit(1)
    print('All required sections are present.')