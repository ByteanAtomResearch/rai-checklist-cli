import importlib.resources
import yaml
import os
import google.generativeai as genai

class TemplateManager:
    def __init__(self, template_file=None):
        if template_file is None:
            with importlib.resources.path('rai_checklist_cli', 'templates.yaml') as p:
                template_file = str(p)
        self.template_file = template_file
        self.templates = self.load_templates()
        self.api_key = None

    def load_templates(self):
        with open(self.template_file, 'r') as f:
            return yaml.safe_load(f)

    def configure_api_key(self):
        self.api_key = input("Enter your Google Gemini API key: ").strip()
        if self.api_key:
            genai.configure(api_key=self.api_key)
            print("API key saved successfully!")
        else:
            print("Please enter a valid API key.")
            self.configure_api_key()

    def generate_checklist_items(self, section_title):
        # Same implementation as before...
        pass  # (Include the method as previously defined)

    def create_section(self, new_template):
        title = input("Enter section title: ").strip()
        generate = input("Generate checklist items using LLM? (y/n): ").strip().lower()
        if generate == 'y':
            items = self.generate_checklist_items(title)
            if items:
                print("Generated Checklist Items:")
                for item in items:
                    print(f"- {item}")
            else:
                print("Failed to generate items.")
                items = []
        else:
            items = []
            print("Enter checklist items (type 'done' when finished):")
            while True:
                item = input("- ").strip()
                if item.lower() == 'done':
                    break
                items.append(item)
        if title and items:
            new_template[title] = {
                'title': title,
                'items': items
            }
            print(f"Section '{title}' added to the template.")
        else:
            print("Section title and items are required.")
            self.create_section(new_template)

    def create_template(self):
        self.configure_api_key()
        name = input("Enter template name: ").strip()
        new_template = {}
        while True:
            add_section = input("Add a section? (y/n): ").strip().lower()
            if add_section == 'y':
                self.create_section(new_template)
            else:
                break
        if new_template:
            self.templates[name] = new_template
            with open(self.template_file, 'w') as f:
                yaml.dump(self.templates, f)
            print(f"Template '{name}' saved successfully!")
        else:
            print("No sections added. Template not saved.")

    def get_available_sections(self, template):
        return list(template.keys())

# Usage
template_manager = TemplateManager()
template_manager.create_template()
