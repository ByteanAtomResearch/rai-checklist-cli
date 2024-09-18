# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0] - 2023-05-24
### Added
- Support for generating checklists in YAML and JSON formats
- CI/CD integration example using GitHub Actions
- New `validate_checklist` function in `rai_checklist_cli/validate_checklist.py`
- Jupyter notebook support with `jupyter_template_manager.py`
- Custom template creation functionality in `template_utils.py`

### Changed
- Updated `checklist_generator.py` to support multiple output formats
- Refactored `cli.py` to improve modularity and add new features
- Updated `setup.py` and `pyproject.toml` to reflect new version and dependencies

### Fixed
- Resolved import issues with `validate_checklist` module

## [0.5.13] - 2023-05-23
### Added
- Initial release of rai-checklist-cli tool
- Basic functionality for generating Responsible AI checklists
- Markdown output support
- Default template for LLM projects

[0.6.0]: https://github.com/ByteanAtomResearch/rai-checklist-cli/compare/v0.5.13...v0.6.0
[0.5.13]: https://github.com/ByteanAtomResearch/rai-checklist-cli/releases/tag/v0.5.13