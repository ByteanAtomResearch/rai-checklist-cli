import pytest
import yaml
from pathlib import Path
from rai_checklist_cli.validate_checklist import validate_checklist, load_config as load_validation_config

# Fixture for the checklist configuration (can be shared via conftest.py if needed)
@pytest.fixture
def test_checklist_config_data():
    return {
        'default': {
            'required_sections': ['SectionA', 'SectionB']
        },
        'critical_ml': {
            'required_sections': ['SectionA']
        },
        'critical_project_types': ['critical_ml'],
        'critical_sections': ['CriticalSection1', 'CriticalSection2']
    }

@pytest.fixture
def test_checklist_config_file(tmp_path, test_checklist_config_data):
    config_file = tmp_path / "test_checklist_config.yaml"
    with open(config_file, 'w') as f:
        yaml.dump(test_checklist_config_data, f)
    return config_file

def create_checklist_yaml_file(tmp_path, filename, content_dict):
    checklist_file = tmp_path / filename
    with open(checklist_file, 'w') as f:
        yaml.dump(content_dict, f)
    return checklist_file

class TestValidateChecklistDirectly:

    def test_valid_critical_project(self, tmp_path, test_checklist_config_file, test_checklist_config_data):
        checklist_content = {
            'SectionA': {'title': 'Section A'},
            'CriticalSection1': {'title': 'Critical Section 1'},
            'CriticalSection2': {'title': 'Critical Section 2'}
        }
        checklist_file = create_checklist_yaml_file(tmp_path, "valid_critical.yaml", checklist_content)
        
        config = load_validation_config(str(test_checklist_config_file))
        is_valid, messages = validate_checklist(str(checklist_file), 'critical_ml', config)
        
        assert is_valid
        assert "All required and critical sections for critical_ml are present." in "".join(messages)

    def test_missing_critical_section(self, tmp_path, test_checklist_config_file, test_checklist_config_data):
        checklist_content = {
            'SectionA': {'title': 'Section A'},
            'CriticalSection1': {'title': 'Critical Section 1'}
            # Missing CriticalSection2
        }
        checklist_file = create_checklist_yaml_file(tmp_path, "missing_critical.yaml", checklist_content)
        
        config = load_validation_config(str(test_checklist_config_file))
        is_valid, messages = validate_checklist(str(checklist_file), 'critical_ml', config)
        
        assert not is_valid
        assert "Missing critical sections for critical_ml: ['CriticalSection2']" in "".join(messages)

    def test_missing_required_section_default_project(self, tmp_path, test_checklist_config_file, test_checklist_config_data):
        checklist_content = {
            'SectionB': {'title': 'Section B'}
            # Missing SectionA
        }
        checklist_file = create_checklist_yaml_file(tmp_path, "missing_required_default.yaml", checklist_content)
        
        config = load_validation_config(str(test_checklist_config_file))
        is_valid, messages = validate_checklist(str(checklist_file), 'default', config)
        
        assert not is_valid
        assert "Missing required sections for default: ['SectionA']" in "".join(messages)

    def test_missing_required_and_critical_sections_critical_project(self, tmp_path, test_checklist_config_file, test_checklist_config_data):
        checklist_content = {
            'SomeOtherSection': {'title': 'Other Section'}
            # Missing SectionA (required for critical_ml)
            # Missing CriticalSection1, CriticalSection2 (critical sections)
        }
        checklist_file = create_checklist_yaml_file(tmp_path, "missing_both.yaml", checklist_content)
        
        config = load_validation_config(str(test_checklist_config_file))
        is_valid, messages = validate_checklist(str(checklist_file), 'critical_ml', config)
        
        assert not is_valid
        messages_str = "".join(messages)
        assert "Missing required sections for critical_ml: ['SectionA']" in messages_str
        # Order of critical sections in message might vary, so check for both
        assert "Missing critical sections for critical_ml:" in messages_str
        assert "CriticalSection1" in messages_str
        assert "CriticalSection2" in messages_str
        
    def test_project_type_not_in_config_uses_default(self, tmp_path, test_checklist_config_file, test_checklist_config_data):
        checklist_content = {
             # Missing SectionA, SectionB (required for default)
        }
        checklist_file = create_checklist_yaml_file(tmp_path, "empty_checklist.yaml", checklist_content)
        config = load_validation_config(str(test_checklist_config_file))
        is_valid, messages = validate_checklist(str(checklist_file), 'new_project_type_not_in_config', config)

        assert not is_valid
        assert "Missing required sections for new_project_type_not_in_config: ['SectionA', 'SectionB']" in "".join(messages)

    def test_empty_checklist_critical_project(self, tmp_path, test_checklist_config_file, test_checklist_config_data):
        checklist_content = {} # Empty checklist
        checklist_file = create_checklist_yaml_file(tmp_path, "empty_critical.yaml", checklist_content)
        
        config = load_validation_config(str(test_checklist_config_file))
        is_valid, messages = validate_checklist(str(checklist_file), 'critical_ml', config)
        
        assert not is_valid
        messages_str = "".join(messages)
        assert "Missing required sections for critical_ml: ['SectionA']" in messages_str
        assert "Missing critical sections for critical_ml:" in messages_str
        assert "CriticalSection1" in messages_str
        assert "CriticalSection2" in messages_str

    def test_config_missing_critical_project_types(self, tmp_path, test_checklist_config_data):
        # Modify config to remove critical_project_types
        del test_checklist_config_data['critical_project_types']
        config_file = tmp_path / "no_crit_types_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(test_checklist_config_data, f)

        checklist_content = { 'SectionA': {} } # Satisfies critical_ml's direct requirements
        checklist_file = create_checklist_yaml_file(tmp_path, "checklist.yaml", checklist_content)
        
        config = load_validation_config(str(config_file))
        is_valid, messages = validate_checklist(str(checklist_file), 'critical_ml', config)
        
        assert is_valid # Should be valid as 'critical_ml' is not considered critical anymore
        assert "All required sections for critical_ml are present." in "".join(messages)
        assert "critical sections" not in "".join(messages).lower() # Ensure no mention of critical sections

    def test_config_missing_critical_sections_list(self, tmp_path, test_checklist_config_data):
        # Modify config to remove critical_sections list
        del test_checklist_config_data['critical_sections']
        config_file = tmp_path / "no_crit_sections_list_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(test_checklist_config_data, f)

        checklist_content = { 'SectionA': {} } # Satisfies critical_ml's direct requirements
        checklist_file = create_checklist_yaml_file(tmp_path, "checklist.yaml", checklist_content)
        
        config = load_validation_config(str(config_file))
        is_valid, messages = validate_checklist(str(checklist_file), 'critical_ml', config)
        
        assert is_valid # Valid because critical_ml is critical, but there are no critical sections to check
        assert 'Project type "critical_ml" is critical. Validating critical sections.' in "".join(messages)
        assert "All required and critical sections for critical_ml are present." in "".join(messages)

```
