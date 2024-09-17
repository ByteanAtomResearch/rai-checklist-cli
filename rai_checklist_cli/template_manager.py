import yaml

class TemplateManager:
    def __init__(self, template_file='templates.yaml'):
        self.template_file = template_file
        self.templates = self.load_templates()

    def load_templates(self):
        with open(self.template_file, 'r') as f:
            return yaml.safe_load(f)

    def get_available_templates(self):
        return list(self.templates.keys())

    def get_template(self, template_name):
        return self.templates.get(template_name, {})

    def save_template(self, template_name, template_data):
        self.templates[template_name] = template_data
        with open(self.template_file, 'w') as f:
            yaml.dump(self.templates, f)