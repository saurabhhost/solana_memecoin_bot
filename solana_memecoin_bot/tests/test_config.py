import pytest
import os
import json
from src.config import load_config, save_config

@pytest.fixture
def temp_config(tmp_path):
    """Create a temporary config file for testing."""
    config_path = tmp_path / "config.json"
    default_config = {
        "blacklist_coins": ["TEST123"],
        "filters": {"min_liquidity": 1000},
        "telegram": {"bot_token": "test_token", "chat_id": "test_chat"}
    }
    with open(config_path, 'w') as f:
        json.dump(default_config, f)
    original_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    os.rename(config_path, original_path)
    yield original_path
    if os.path.exists(original_path):
        os.remove(original_path)

def test_load_config_default(tmp_path):
    """Test loading config when file doesn't exist."""
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')
    if os.path.exists(config_path):
        os.remove(config_path)
    config = load_config()
    assert "blacklist_coins" in config
    assert "telegram" in config
    assert config["filters"]["min_liquidity"] == 1000
    assert os.path.exists(config_path)  # Default config should be created

def test_load_config_existing(temp_config):
    """Test loading an existing config file."""
    config = load_config()
    assert config["blacklist_coins"] == ["TEST123"]
    assert config["telegram"]["bot_token"] == "test_token"

def test_save_config(temp_config):
    """Test saving updated config."""
    config = load_config()
    config["blacklist_coins"].append("NEW456")
    save_config(config)
    updated_config = load_config()
    assert "NEW456" in updated_config["blacklist_coins"]
