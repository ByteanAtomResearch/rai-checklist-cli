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
    if custom_checklist:
        with open(custom_checklist, 'r') as file:
            template = yaml.safe_load(file)
    
    if file_format not in ["md", "yaml"]:
        raise ValueError(f"Unsupported file format: {file_format}")
    
    template_name = template.get('name', '')
    full_title = f"{title} - {template_name}" if template_name else title

    checklist_dict = {template[section]['title']: template[section]['items'] for section in sections if section in template}
    
    if file_format == "md":
        checklist = f"# {full_title}\n\n"
        for section_title, items in checklist_dict.items():
            checklist += f"## {section_title}\n"
            for item in items:
                checklist += f"- [ ] {item}\n"
            checklist += "\n"
        return checklist
    elif file_format == "yaml":
        return yaml.dump(checklist_dict, sort_keys=False)