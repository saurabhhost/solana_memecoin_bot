import json
import os

def load_config():
    """Load configuration from config.json, create default if not found."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        default_config = {
            "blacklist_coins": [],
            "blacklist_devs": [],
            "filters": {
                "min_liquidity": 1000,
                "min_volume": 5000,
                "min_safety_score": 85
            },
            "telegram": {
                "bot_token": "YOUR_TOXI_BOT_TOKEN",
                "chat_id": "YOUR_CHAT_ID"
            },
            "trading": {
                "min_buy_sol": 0.01,
                "max_buy_sol": 0.15,
                "slippage": 30,
                "profit_target": 10
            }
        }
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config

def save_config(config):
    """Save updated configuration to config.json."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
