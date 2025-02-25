import json
import os

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        default_config = {
            "telegram": {
                "bot_token": "7923440418:AAEC1kgH13he8X0LMXXHzl-l_Gr1yMGAyoc",
                "chat_id": "1836363133",
                "api_id": 21324591,
                "api_hash": "46db11d681dfb307167f4d2811e1934a",
                "phone_number": "+917258065221"
            },
            # ... other config fields ...
        }
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config

def save_config(config):
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
