import importlib.resources
import yaml
import os
from typing import List, Optional, Dict, Union
import google.generativeai as genai
from .checklist_generator import generate_checklist
from .colab_utils import is_running_in_colab, save_to_storage, load_from_storage

class JupyterTemplateManager:
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

    def generate_template_sections(self, template_name: str) -> Dict[str, Dict[str, Union[str, List[str]]]]:
        if not self.api_key:
            self.configure_api_key()
        
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""Generate a template for a '{template_name}' Responsible AI Checklist. 
        The template should have 5-8 sections, each with a title and 3-5 checklist items.
        Follow this exact YAML format for each section:

        section_key:
          title: "Section Title"
          items:
            - "Checklist item 1"
            - "Checklist item 2"
            - "Checklist item 3"

        Ensure each section_key is a lowercase, underscore-separated version of the title.
        Make the sections and items specific to {template_name} and cover various aspects of responsible AI development."""
        
        response = model.generate_content(prompt)
        try:
            generated_template = yaml.safe_load(response.text)
            return generated_template
        except yaml.YAMLError:
            print("Error parsing generated template. Using fallback method.")
            return self.fallback_generate_template(template_name)

    def fallback_generate_template(self, template_name: str) -> Dict[str, Dict[str, Union[str, List[str]]]]:
        sections = [
            "project_motivation",
            "problem_definition",
            "ethical_considerations",
            "data_preparation",
            "model_development",
            "evaluation_and_testing",
            "deployment_and_monitoring"
        ]
        
        template = {}
        for section in sections:
            title = " ".join(word.capitalize() for word in section.split("_"))
            template[section] = {
                "title": title,
                "items": self.generate_checklist_items(title, template_name)
            }
        
        return template

    def generate_checklist_items(self, section_title: str, template_name: str) -> List[str]:
        if not self.api_key:
            self.configure_api_key()
        
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"""Generate 3-5 checklist items for the section titled '{section_title}' in a '{template_name}' Responsible AI Checklist. 
        Each item should be a concise, actionable task or question.
        Format each item as a string in a YAML list, like this:
        - "Checklist item 1"
        - "Checklist item 2"
        - "Checklist item 3"
        
        Ensure the items are specific to {template_name} and cover different aspects of {section_title}."""
        
        response = model.generate_content(prompt)
        try:
            items = yaml.safe_load(response.text)
            if isinstance(items, list) and all(isinstance(item, str) for item in items):
                return items
            else:
                raise ValueError("Generated items are not in the correct format")
        except (yaml.YAMLError, ValueError):
            print(f"Error parsing generated items for {section_title}. Using fallback method.")
            return [f"Item 1 for {section_title}", f"Item 2 for {section_title}", f"Item 3 for {section_title}"]

    def create_template(self):
        name = input("Enter template name: ").strip()
        print(f"Generating template for '{name}'...")
        
        new_template = self.generate_template_sections(name)
        
        print("\nGenerated template:")
        for section, content in new_template.items():
            print(f"\n{content['title']}:")
            for item in content['items']:
                print(f"  - {item}")
        
        edit = input("\nWould you like to edit this template? (y/n): ").strip().lower()
        if edit == 'y':
            new_template = self.edit_template(new_template)
        
        if new_template:
            self.templates[name] = new_template
            with open(self.template_file, 'w') as f:
                yaml.dump(self.templates, f)
            print(f"Template '{name}' saved successfully!")
        else:
            print("No sections added. Template not saved.")

    def edit_template(self, template: Dict[str, Dict[str, Union[str, List[str]]]]) -> Dict[str, Dict[str, Union[str, List[str]]]]:
        while True:
            print("\nCurrent sections:")
            for i, (section, content) in enumerate(template.items(), 1):
                print(f"{i}. {content['title']}")
            
            action = input("Enter 'e' to edit a section, 'a' to add a new section, or 'd' when done: ").strip().lower()
            if action == 'e':
                self.edit_section(template)
            elif action == 'a':
                self.add_section(template)
            elif action == 'd':
                break
            else:
                print("Invalid input. Please try again.")
        
        return template

    def edit_section(self, template: Dict[str, Dict[str, Union[str, List[str]]]]):
        section_index = int(input("Enter the number of the section to edit: ")) - 1
        sections = list(template.keys())
        if 0 <= section_index < len(sections):
            section_key = sections[section_index]
            section = template[section_key]
            
            print(f"\nEditing section: {section['title']}")
            new_title = input(f"Enter new title (or press Enter to keep '{section['title']}'): ").strip()
            if new_title:
                section['title'] = new_title
            
            print("\nCurrent items:")
            for i, item in enumerate(section['items'], 1):
                print(f"{i}. {item}")
            
            section['items'] = self.edit_items(section['items'])
            print(f"Section '{section['title']}' updated.")
        else:
            print("Invalid section number.")

    def add_section(self, template: Dict[str, Dict[str, Union[str, List[str]]]]):
        title = input("Enter section title: ").strip()
        key = "_".join(title.lower().split())
        items = self.generate_checklist_items(title, "custom section")
        
        print("\nGenerated checklist items:")
        for i, item in enumerate(items, 1):
            print(f"{i}. {item}")
        
        edit = input("Would you like to edit these items? (y/n): ").strip().lower()
        if edit == 'y':
            items = self.edit_items(items)
        
        template[key] = {
            'title': title,
            'items': items
        }
        print(f"Section '{title}' added to the template.")

    def edit_items(self, items: List[str]) -> List[str]:
        print("Edit items (press Enter to keep, enter new text to modify, or 'd' to delete):")
        edited_items = []
        for i, item in enumerate(items, 1):
            while True:
                edit = input(f"{i}. {item}: ").strip()
                if edit.lower() == 'd':
                    break
                elif edit:
                    edited_items.append(edit)
                    break
                else:
                    edited_items.append(item)
                    break
        
        while True:
            new_item = input("Enter a new item (or press Enter to finish): ").strip()
            if new_item:
                edited_items.append(new_item)
            else:
                break
        
        return edited_items

    def get_available_templates(self) -> List[str]:
        return list(self.templates.keys())

    def display_available_templates(self):
        templates = self.get_available_templates()
        print("Available templates:")
        for i, template in enumerate(templates, 1):
            print(f"{i}. {template}")

    def generate_checklist(self, template_name: str, file_format: str, output_file: Optional[str] = None):
        if template_name not in self.templates:
            print(f"Template '{template_name}' not found.")
            return

        template = self.templates[template_name]
        sections = list(template.keys())
        checklist = generate_checklist(template, sections, file_format)

        if output_file:
            saved_path = save_to_storage(output_file, checklist)
            if saved_path:
                print(f"Checklist saved to {saved_path}")
        else:
            print(checklist)

        if is_running_in_colab():
            save_to_colab = input("Save to Google Colab storage? (y/n): ").strip().lower()
            if save_to_colab == 'y':
                filename = input("Enter filename for Colab storage: ").strip()
                save_to_storage(filename, checklist)

    def run(self):
        while True:
            print("\nRAI Checklist Template Manager")
            print("1. Create new template")
            print("2. Generate checklist from existing template")
            print("3. Exit")
            choice = input("Enter your choice (1-3): ").strip()

            if choice == '1':
                self.create_template()
            elif choice == '2':
                self.display_available_templates()
                template_name = input("Enter the name of the template to use: ").strip()
                file_format = input("Enter output format (md/yaml): ").strip().lower()
                output_file = input("Enter output file name (or press Enter to print to console): ").strip()
                self.generate_checklist(template_name, file_format, output_file if output_file else None)
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

# Usage
if __name__ == "__main__":
    template_manager = JupyterTemplateManager()
    template_manager.run()