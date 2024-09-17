import importlib.resources
import yaml
import ipywidgets as widgets
from IPython.display import display

class JupyterTemplateManager:
    def __init__(self, template_file=None):
        if template_file is None:
            with importlib.resources.path('rai_checklist_cli', 'templates.yaml') as p:
                template_file = str(p)
        self.template_file = template_file
        self.templates = self.load_templates()

    def load_templates(self):
        with open(self.template_file, 'r') as f:
            return yaml.safe_load(f)

    def create_section(self):
        section_title = widgets.Text(
            value='',
            placeholder='Enter section title',
            description='Section Title:',
            disabled=False
        )
        
        section_items = widgets.Textarea(
            value='',
            placeholder='Enter checklist items, one per line',
            description='Checklist Items:',
            disabled=False
        )
        
        display(section_title, section_items)
        
        return section_title, section_items

    def create_template(self):
        template_name = widgets.Text(
            value='',
            placeholder='Enter template name',
            description='Template Name:',
            disabled=False
        )
        add_section_button = widgets.Button(description="Add Section")
        save_template_button = widgets.Button(description="Save Template")
        
        display(template_name, add_section_button, save_template_button)
        
        new_template = {}
        
        def add_section(b):
            section_title, section_items = self.create_section()
            items_list = section_items.value.split('\n')
            new_template[section_title.value] = {
                'title': section_title.value,
                'items': items_list
            }
        
        def save_template(b):
            self.templates[template_name.value] = new_template
            with open(self.template_file, 'w') as f:
                yaml.dump(self.templates, f)
            print(f'Template {template_name.value} saved successfully!')
        
        add_section_button.on_click(add_section)
        save_template_button.on_click(save_template)

# Create an instance to use in the notebook
template_manager = JupyterTemplateManager()

# Create a new template
template_manager.create_template()
