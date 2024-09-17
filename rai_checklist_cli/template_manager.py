import yaml
import importlib.resources
import os
import logging

logger = logging.getLogger(__name__)

class TemplateManager:
    def __init__(self, template_file=None):
        self.template_file = template_file
        self.templates = self.load_templates()

    def load_templates(self):
        if self.template_file:
            logger.debug(f"Loading custom template file: {self.template_file}")
            return self._load_from_file(self.template_file)
        else:
            logger.debug("Attempting to load default templates.yaml")
            return self._load_default_templates()

    def _load_from_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Template file not found: {file_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing YAML in {file_path}: {e}")
            raise

    def _load_default_templates(self):
        try:
            with importlib.resources.path('rai_checklist_cli', 'templates.yaml') as template_path:
                return self._load_from_file(template_path)
        except ImportError:
            logger.error("Unable to locate default templates.yaml in package")
            raise FileNotFoundError("Default templates.yaml not found in package")

    def get_available_templates(self):
        return list(self.templates.keys())

    def get_template(self, template_name):
        return self.templates.get(template_name, {})

    def save_template(self, template_name, template_data):
        self.templates[template_name] = template_data
        if self.template_file:
            with open(self.template_file, 'w') as f:
                yaml.dump(self.templates, f)
        else:
            logger.warning("Cannot save template when using package resources.")