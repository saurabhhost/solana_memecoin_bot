import pytest
import sqlite3
from src.database import init_db, store_coin, update_entry_price, get_coin

@pytest.fixture
def db_setup(tmp_path):
    """Set up a temporary database for testing."""
    db_path = tmp_path / "memecoins.db"
    original_path = os.path.join(os.path.dirname(__file__), '..', 'memecoins.db')
    if os.path.exists(original_path):
        os.remove(original_path)
    sqlite3.connect(str(db_path)).close()
    os.rename(db_path, original_path)
    yield
    if os.path.exists(original_path):
        os.remove(original_path)

def test_init_db(db_setup):
    """Test database initialization."""
    init_db()
    conn = sqlite3.connect('memecoins.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='coins'")
    assert c.fetchone() is not None
    conn.close()

def test_store_and_get_coin(db_setup):
    """Test storing and retrieving a coin."""
    init_db()
    store_coin("TEST123", "TestCoin", 2000, 6000)
    coin = get_coin("TEST123")
    assert coin["token_address"] == "TEST123"
    assert coin["name"] == "TestCoin"
    assert coin["liquidity"] == 2000
    assert coin["volume"] == 6000

def test_update_entry_price(db_setup):
    """Test updating entry price."""
    init_db()
    store_coin("TEST123", "TestCoin", 2000, 6000)
    update_entry_price("TEST123", 0.05)
    coin = get_coin("TEST123")
    assert coin["entry_price"] == 0.05
