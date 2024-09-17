import os
import yaml

CONFIG_FILE = os.path.expanduser('~/.rai_checklist_config.yaml')

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

config = load_config()
