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

To validate a checklist against project requirements:

```bash
rai-checklist validate path/to/your/checklist.yaml --project-type machine_learning
```

## 7. CI/CD Integration

The tool can be integrated into CI/CD pipelines. An example GitHub Actions workflow is provided in the repository.

## 8. Jupyter Notebook Usage

The tool can be used within Jupyter notebooks. Import the necessary modules:

```python
from rai_checklist_cli.checklist_generator import generate_checklist
import yaml
```

Then use the `generate_checklist` function to create checklists programmatically.

## 9. Configuration

The tool uses a configuration file located at `~/.rai_checklist_config.yaml`. You can specify custom paths or settings in this file.

## 10. Troubleshooting

If you encounter issues:

- Ensure you have the latest version installed
- Check that all dependencies are correctly installed
- Verify that your custom templates or configuration files are correctly formatted

For more help, please open an issue on the GitHub repository.