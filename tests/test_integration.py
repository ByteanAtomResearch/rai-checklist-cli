# test_integration.py

import subprocess
import json
import yaml

def test_integration():
    # Generate a checklist using CLI
    subprocess.run(["rai-checklist", "generate", "-o", "test_integration.json", "-f", "json"])

    # Load the generated checklist programmatically
    with open("test_integration.json", "r") as f:
        checklist_data = json.load(f)

    # Verify the loaded data
    assert isinstance(checklist_data, dict), "Loaded data is not a dictionary"
    assert len(checklist_data) > 0, "Loaded checklist is empty"

    # Manipulate the data
    first_section = list(checklist_data.keys())[0]
    checklist_data[first_section].append("New test item")

    # Save the modified checklist
    with open("test_modified.yaml", "w") as f:
        yaml.dump(checklist_data, f)

    print("Integration test passed successfully")

if __name__ == "__main__":
    test_integration()
