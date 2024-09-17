def create_custom_template(template_manager):
    template_name = input("Enter a name for your custom template: ").strip()
    if template_name in template_manager.get_available_templates():
        overwrite = input(f"Template '{template_name}' already exists. Do you want to overwrite it? (y/n): ").lower()
        if overwrite != 'y':
            print("Template creation cancelled.")
            return

    template_data = {}
    while True:
        section_name = input("Enter a section name (or press Enter to finish): ").strip()
        if not section_name:
            break

        section_title = input(f"Enter the title for '{section_name}': ").strip()
        items = []
        print(f"Enter items for '{section_name}' (one per line, press Enter twice to finish):")
        while True:
            item = input().strip()
            if not item:
                break
            items.append(item)

        template_data[section_name] = {
            'title': section_title,
            'items': items
        }

    template_manager.save_template(template_name, template_data)

def display_available_templates(templates):
    print("Available Templates and Sections:")
    for template_name, sections in templates.items():
        print(f"Template: {template_name}")
        for section_name, section_content in sections.items():
            print(f"  - Section: {section_content['title']}")

def focus_on_section(templates, selected_template, selected_section):
    if selected_template not in templates:
        print(f"Template '{selected_template}' not found.")
        return

    template = templates[selected_template]
    if selected_section not in template:
        print(f"Section '{selected_section}' not found in template '{selected_template}'.")
        return

    section = template[selected_section]
    print(f"Focused Section: {section['title']}")
    for item in section['items']:
        print(f"- {item}")