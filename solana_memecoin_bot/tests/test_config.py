import pytest
from src.config import load_config, save_config

def test_load_config():
    config = load_config()
    assert "blacklist_coins" in config
    assert "telegram" in config
