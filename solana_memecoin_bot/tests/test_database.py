import pytest
from src.database import init_db, store_coin, get_coin

def test_database():
    init_db()
    store_coin("TEST123", "TestCoin", 2000, 6000)
    coin = get_coin("TEST123")
    assert coin["name"] == "TestCoin"
