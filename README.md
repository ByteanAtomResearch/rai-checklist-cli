# Responsible AI Checklist CLI

[![PyPI version](https://badge.fury.io/py/rai-checklist-cli.svg)](https://badge.fury.io/py/rai-checklist-cli)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/rai-checklist-cli.svg)](https://pypi.org/project/rai-checklist-cli)

A command-line tool to easily add customizable responsible AI checklists to data science, Generative AI, or traditional machine learning projects. This tool helps ensure that AI projects adhere to ethical guidelines and best practices throughout their lifecycle. 

This CLI compliments the RAI Auditor UI currently in development.

![RAI Checklist UI Screenshot](https://github.com/ByteanAtomResearch/rai-checklist-cli/raw/main/images/rai-checklist-ui-screenshot.png)

<!-- ![RAI Checklist CLI Screenshot](./images/rai-checklist-cli-screenshot.png) -->

## Features

- Generate customizable AI responsibility checklists
- Support for various output formats: Markdown (`.md`), YAML (`.yaml`), JSON (`.json`).
- Easily integrate into existing projects or CI/CD pipelines.
- Customizable checklist sections
- Validation of ethical and technical aspects in CI/CD pipelines using YAML or JSON checklists.

## New Features Added:

- **Support for YAML and JSON:** You can now generate checklists in YAML and JSON formats, making it easy to integrate into CI/CD pipelines.
- **CI/CD Integration Example:** Added GitHub Actions template to automate responsible AI checks.

## Installation

Install the Responsible AI Checklist CLI using pip:

```bash
pip install rai-checklist-cli
```
Note: that PyYAML is a dependency. You may have to install that separately. Known issue.

## Usage

The basic syntax for using the CLI is:

```
rai-checklist [OPTIONS]
```

Options:

- `-h, --help`: Show help message and exit
- `-w, --overwrite`: Overwrite existing output file
- `-o, --output PATH`: Specify output file path
- `-f, --format TEXT`: Specify output format (md, yaml, json)
- `-l, --checklist PATH`: Path to custom checklist file
- `--project-type TEXT`: Specify project type for validation (default, machine_learning, web_application, etc.)
- `--config PATH`: Path to the configuration file for validation

## Examples

Generate a markdown checklist:

```
rai-checklist -o checklist.md -f md
```

Generate a YAML checklist:

```
rai-checklist -o checklist.yaml -f yaml
```

Generate a JSON checklist:

```
rai-checklist -o checklist.json -f json
```

Validate a checklist for a machine learning project:

```
rai-checklist -o checklist.yaml -f yaml --project-type machine_learning
```

## Integration into CI/CD Pipelines

You can leverage the YAML or JSON output formats to automate responsible AI checks in your CI/CD pipelines, ensuring ethical and performance guidelines are met before deployment.

## Example GitHub Action:

Here's how you can use the rai-checklist-cli in GitHub Actions to automatically validate your AI project's responsible AI checklist.

Create a `.github/workflows/ai-responsibility-check.yml` file with the following content:

```yaml
name: Responsible AI Checklist CI

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  responsibility_checklist:
    runs-on: ubuntu-latest

    steps:
    # Step 1: Checkout repository
    - name: Checkout repository
      uses: actions/checkout@v2

    # Step 2: Set up Python environment
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    # Step 3: Install the checklist CLI and dependencies
    - name: Install dependencies
      run: |
        pip install rai-checklist-cli pyyaml

    # Step 4: Generate the Responsible AI Checklist in YAML format
    - name: Generate YAML Checklist
      run: |
        rai-checklist -o responsible_ai_checklist.yaml -f yaml

    # Step 5: Validate the checklist
    - name: Validate Checklist
      run: |
        python -c "
import yaml
with open('responsible_ai_checklist.yaml') as f:
    checklist = yaml.safe_load(f)
    required_sections = ['Ethical considerations', 'Deployment and Monitoring']
    missing_sections = [s for s in required_sections if s not in checklist['sections']]
    if missing_sections:
        print(f'Missing required sections: {missing_sections}')
        exit(1)
    else:
        print('All required sections are present.')
        "
```

### How It Works:

- Generate YAML Checklist: The CLI generates a YAML checklist as part of your CI/CD process.
- Validate Checklist: The action reads the YAML checklist and ensures that critical sections (like "Ethical considerations" and "Deployment Monitoring") are present. If any section is missing, the pipeline will fail, enforcing responsible AI practices.

## Stages

The default checklist includes the following stages of the AI/ML lifecycle:

- Project Motivation
- Problem Definition
- Performance Measurement
- LLM-Specific Evaluation Metrics
- Ethical Considerations
- Roadmap/Timeline
- Contacts/Stakeholders
- Collaboration
- User Research Aspects
- End User Definition
- End User Testing
- Deployment and Monitoring
- Continual Improvement

## Customization

You can customize the checklist by creating a YAML or JSON file with your desired sections and items. Use the `-l` or `--checklist` option to specify your custom checklist file when running the CLI.

For more information on creating custom checklists, please refer to the [documentation](https://github.com/ByteanAtomResearch/rai-checklist-cli/wiki/Custom-Checklists).

## Contributing

Contributions are welcome! Here's how you can contribute to the project:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin feature/your-feature-name`)
6. Create a new Pull Request

Please make sure to update tests as appropriate and adhere to the [code of conduct](CODE_OF_CONDUCT.md).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project was inspired by and builds upon the work of several existing tools and individuals:

* [Deon](https://deon.drivendata.org/) by [DrivenData](https://www.drivendata.org/): An ethics checklist for data scientists.
* [CAITI AI Risk Library](https://github.com/byteanatom/caiti-ai-risk-library) by ByteanAtom Research: A comprehensive library for AI risk assessment.

### Contributors

* [Noble Ackerson](https://www.linkedin.com/in/noblea) : Project lead and main contributor.

We're grateful for the open-source community and the valuable resources that have made this project possible.

---

**Note:** This project is currently in development. Features and documentation may be incomplete or subject to change.

TODO:
- [x] Complete the documentation for custom checklists
- [x] Add more examples and use cases
- [ ] Include frontend-UI (see screenshot)
- [x] Set up continuous integration and testing
- [x] Add detailed contribution guidelines