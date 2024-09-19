import json
import yaml
from typing import Dict, Union, List, Optional

def generate_section(section_data):
    section = f"## {section_data['title']}\n"
    for item in section_data['items']:
        section += f"- [ ] {item}\n"
    return section + "\n"

def generate_checklist(template: Dict[str, Dict[str, Union[str, List[str]]]], 
                       sections: List[str], 
                       file_format: str, 
                       title: str = "Responsible AI Checklist for LLM Projects",
                       custom_checklist: Optional[str] = None) -> str:
    # Handle custom_checklist if provided
    if custom_checklist:
        # Load custom checklist and use it instead of the template
        with open(custom_checklist, 'r') as file:
            custom_template = yaml.safe_load(file)
        template = custom_template
    
    if file_format not in ["md", "yaml", "json"]:
        raise ValueError(f"Unsupported file format: {file_format}")
    
    if file_format == "md":
        checklist = f"# {title}\n\n"
        for section in sections:
            if section in template:
                checklist += generate_section(template[section])
            else:
                print(f"Warning: Section '{section}' is not in the template and will be skipped.")
        return checklist

    checklist_dict = {template[section]['title']: template[section]['items'] for section in sections if section in template}
    
    if file_format == "yaml":
        return yaml.dump(checklist_dict, sort_keys=False)
    elif file_format == "json":
        return json.dumps(checklist_dict, indent=2)