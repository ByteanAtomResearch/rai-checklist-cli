# test_integration.py

import subprocess
import yaml
import os
import tempfile
import pytest

def test_integration():
    with tempfile.TemporaryDirectory() as tmpdirname:
        for file_format in ["md", "yaml"]:
            output_file = os.path.join(tmpdirname, f"test_integration.{file_format}")
            
            try:
                result = subprocess.run(
                    ["rai-checklist", "generate", "-o", output_file, "-f", file_format, "-s", "problem_definition", "ethical_considerations"],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=tmpdirname
                )
                
                print(f"STDOUT ({file_format}):", result.stdout)
                print(f"STDERR ({file_format}):", result.stderr)
                
                assert os.path.exists(output_file), f"Output file {output_file} does not exist"
                
                with open(output_file, "r") as f:
                    content = f.read()
                
                if file_format == "md":
                    assert "# Responsible AI Checklist for ML & AI Projects" in content
                    assert "## Problem Definition" in content
                    assert "## Ethical Considerations" in content
                elif file_format == "yaml":
                    checklist_data = yaml.safe_load(content)
                    assert "Problem Definition" in checklist_data
                    assert "Ethical Considerations" in checklist_data
                
            except subprocess.CalledProcessError as e:
                print(f"Command failed with return code ({file_format})", e.returncode)
                print(f"STDOUT ({file_format}):", e.stdout)
                print(f"STDERR ({file_format}):", e.stderr)
                pytest.fail(f"rai-checklist generate command failed for {file_format}")

if __name__ == "__main__":
    test_integration()
