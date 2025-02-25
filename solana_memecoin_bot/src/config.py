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
                "bot_token": "YOUR_TOXI_BOT_TOKEN",
                "chat_id": "YOUR_CHAT_ID",
                "api_id": 1234567,
                "api_hash": "your_api_hash_here",
                "phone_number": "+1234567890"
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
