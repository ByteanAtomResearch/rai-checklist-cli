import importlib.resources
import yaml
import os
import google.generativeai as genai
from typing import List, Optional
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
        self.configure_api_key()

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

    def generate_checklist_items(self, section_title: str) -> List[str]:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Generate a list of 5-10 checklist items for a section titled '{section_title}' in a Responsible AI Checklist for LLM Projects. Each item should be a concise, actionable task."
        response = model.generate_content(prompt)
        items = response.text.strip().split('\n')
        return [item.lstrip('- ') for item in items if item.strip()]

    def create_section(self, new_template):
        title = input("Enter section title: ").strip()
        generate = input("Generate checklist items using LLM? (y/n): ").strip().lower()
        if generate == 'y':
            items = self.generate_checklist_items(title)
            if items:
                print("Generated Checklist Items:")
                for item in items:
                    print(f"- {item}")
                edit = input("Would you like to edit these items? (y/n): ").strip().lower()
                if edit == 'y':
                    items = self.edit_items(items)
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

    def edit_items(self, items: List[str]) -> List[str]:
        print("Edit items (press Enter to keep, or type new text to modify):")
        edited_items = []
        for item in items:
            edit = input(f"{item}: ").strip()
            edited_items.append(edit if edit else item)
        return edited_items

    def create_template(self):
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
                print(f"Checklist saved to Colab storage as '{filename}'")

    def run(self):
        while True:
            print("\n1. Create new template")
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