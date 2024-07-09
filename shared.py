import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIGS_PATH = os.path.join(SCRIPT_DIR, "config.json")

def get_config() -> dict[str, dict]:
    with open(CONFIGS_PATH, "r") as config_file:
        return json.loads(config_file.read())
