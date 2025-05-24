# Usage Guide for rai-checklist-cli

## 1. Installation

Install the Responsible AI Checklist CLI using pip:

```bash
pip install rai-checklist-cli
```

Note: PyYAML is a dependency. You may need to install it separately if you encounter issues.

## 2. Basic Usage

**The basic syntax for using the CLI is:**

```bash
rai-checklist [OPTIONS]
```

**To generate a default checklist:**
```bash
rai-checklist generate
```

## 3. Command-Line Options

- `-h, --help`: Show help message and exit
- `-w, --overwrite`: Overwrite existing output file
- `-o, --output PATH`: Specify output file path
- `-f, --format TEXT`: Specify output format (md, yaml, json)
- `-l, --checklist PATH`: Path to custom checklist file
- `--project-type TEXT`: Specify project type for validation (default, machine_learning, web_application, etc.)
- `--config PATH`: Path to the configuration file for validation

## 4. Output Formats

The tool supports three output formats:

- Markdown (md)
- YAML
- JSON

Specify the format using the `-f` or `--format` option:

```bash
rai-checklist generate -f yaml
```

## 5. Custom Templates

To create a custom template:

```bash
rai-checklist create-template
```


Follow the prompts to name your template and add sections and items.

To use a custom template:

```bash
rai-checklist generate -t your_custom_template
```

## 6. Validation

The CLI offers two main ways to validate your checklists:

1.  **Direct Validation**: Use the `validate` command to check an existing checklist file against project requirements.
    ```bash
    rai-checklist validate path/to/your/checklist.yaml --project-type machine_learning --config path/to/your/checklist_config.yaml
    ```
    This command will check if the sections in `path/to/your/checklist.yaml` meet the requirements defined in your configuration for the `machine_learning` project type.

2.  **Automatic Validation during Generation**: When generating a checklist in YAML format with a specified project type, the CLI automatically validates the newly generated checklist.

## 7. Advanced Checklist Validation

The CLI includes an advanced validation feature to ensure critical sections are not overlooked in important projects. This is configured via the `checklist_config.yaml` file (or a custom config specified with `--config`).

### Configuration

You can define which project types are considered critical and which sections are mandatory for them within your `checklist_config.yaml`:

```yaml
# In your checklist_config.yaml (or a custom --config file)
default:
  required_sections:
    - 'Ethical considerations'

machine_learning: # A standard project type
  required_sections:
    - 'Data Privacy'
    - 'Model Bias'

# Defines a list of project types that are considered critical.
# For these project types, an additional set of 'critical_sections' must be present.
critical_project_types:
  - 'machine_learning'  # This marks 'machine_learning' as a critical project type.
  - 'ai_assisted_healthcare' # Another example of a critical project type.

# Defines a list of sections that are mandatory for any project type
# listed in 'critical_project_types'.
critical_sections:
  - 'Bias Mitigation Strategies'
  - 'Ethical Review Board Sign-off'
  - 'Detailed Risk Assessment'
```

When a project type specified with `--project-type` during generation (or validation) is listed in `critical_project_types`, the validation process will ensure that all sections from `critical_sections` are present in the checklist, in addition to its regular `required_sections` (as defined under the project type itself, e.g., `machine_learning.required_sections`).

### Automatic Validation with `generate`

If you generate a checklist in YAML format and specify a project type, the validation runs automatically:

```bash
rai-checklist generate -o my_ml_checklist.yaml -f yaml --project-type machine_learning --config path/to/your/checklist_config.yaml
```

After `my_ml_checklist.yaml` is generated, the CLI will output a validation report to the console:

**Example Validation Report (Failure):**
```
--- Checklist Validation Report ---
Project type "machine_learning" is critical. Validating critical sections.
Missing critical sections for machine_learning: ['Detailed Risk Assessment']
Missing required sections for machine_learning: ['Data Privacy']
Checklist validation failed. Please review the messages above.
```

**Example Validation Report (Success):**
```
--- Checklist Validation Report ---
Project type "machine_learning" is critical. Validating critical sections.
All required and critical sections for machine_learning are present.
Checklist validation successful.
```
**Note:** Automatic validation during the `generate` command is currently performed only for YAML output formats. For other formats, or to validate an existing checklist, use the `rai-checklist validate` command.

## 8. CI/CD Integration

The tool can be integrated into CI/CD pipelines. An example GitHub Actions workflow is provided in the repository.

## 9. Jupyter Notebook Usage

The tool can be used within Jupyter notebooks. Import the necessary modules:

```python
from rai_checklist_cli.checklist_generator import generate_checklist
import yaml
```

Then use the `generate_checklist` function to create checklists programmatically.

## 10. Configuration

The CLI looks for a default configuration file named `checklist_config.yaml` in the current working directory or a user-specific directory (e.g., `~/.config/rai_checklist_cli/checklist_config.yaml` - behavior might vary by OS). You can always specify a custom configuration path using the `--config` option with `generate` or `validate` commands.

The `checklist_config.yaml` defines project types and their required checklist sections, as well as critical project designations.

## 11. Troubleshooting

If you encounter issues:

- Ensure you have the latest version installed
- Check that all dependencies are correctly installed
- Verify that your custom templates or configuration files are correctly formatted

For more help, please open an issue on the GitHub repository.