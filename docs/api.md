# rai-checklist-cli API Documentation

## checklist_generator

### generate_checklist

Generates a checklist based on the provided template and sections.

```python
def generate_checklist(template: Dict[str, Dict[str, Union[str, List[str]]]],
sections: List[str],
file_format: str,
title: str = "Responsible AI Checklist for LLM Projects") -> str:
```

#### Parameters:
- `template`: A dictionary containing the checklist template
- `sections`: A list of section names to include in the checklist
- `file_format`: The output format ('md', 'yaml', or 'json')
- `title`: The title of the checklist (default: "Responsible AI Checklist for LLM Projects")

#### Returns:
A string containing the generated checklist in the specified format.

#### Example:
```python
from rai_checklist_cli.checklist_generator import generate_checklist
template = {
"section1": {
"title": "Section 1",
"items": ["Item 1", "Item 2"]
}
}
sections = ["section1"]
checklist = generate_checklist(template, sections, "md")
print(checklist)
```


## template_manager

### TemplateManager

A class for managing checklist templates.

#### Methods:

##### get_template

```python
def get_template(self, template_name: str) -> Dict[str, Any]:
```


Retrieves a template by name.

###### Parameters:
- `template_name`: The name of the template to retrieve

###### Returns:
A dictionary containing the template data.

###### Example:

```python
from rai_checklist_cli.template_manager import TemplateManager
tm = TemplateManager()
template = tm.get_template("default")
print(template)
```

## validate_checklist

### validate_checklist

Validates a checklist against project requirements.

```python
def validate_checklist(checklist_file: str, project_type: str, config: Dict[str, Any]) -> bool:
```

#### Parameters:
- `checklist_file`: Path to the checklist file
- `project_type`: Type of project (e.g., 'machine_learning', 'web_application')
- `config`: Configuration dictionary

#### Returns:
A boolean indicating whether the checklist is valid.

#### Example:

```python
from rai_checklist_cli.validate_checklist import validate_checklist, load_config
config = load_config('path/to/config.yaml')
is_valid = validate_checklist('path/to/checklist.yaml', 'machine_learning', config)
print(f"Checklist is valid: {is_valid}")

```