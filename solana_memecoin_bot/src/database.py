import sqlite3
from datetime import datetime

def init_db():
    """Initialize SQLite database with coins table."""
    conn = sqlite3.connect('memecoins.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS coins 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  token_address TEXT UNIQUE, 
                  name TEXT, 
                  liquidity REAL, 
                  volume REAL, 
                  timestamp TEXT, 
                  entry_price REAL)''')
    conn.commit()
    conn.close()

def store_coin(token_address, name, liquidity, volume):
    """Store or update coin data in the database."""
    conn = sqlite3.connect('memecoins.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO coins (token_address, name, liquidity, volume, timestamp)
                 VALUES (?, ?, ?, ?, ?)''', 
              (token_address, name, liquidity, volume, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def update_entry_price(token_address, entry_price):
    """Update the entry price for a coin."""
    conn = sqlite3.connect('memecoins.db')
    c = conn.cursor()
    c.execute('UPDATE coins SET entry_price = ? WHERE token_address = ?', (entry_price, token_address))
    conn.commit()
    conn.close()

def get_coin(token_address):
    """Retrieve coin data by token address."""
    conn = sqlite3.connect('memecoins.db')
    c = conn.cursor()
    c.execute('SELECT * FROM coins WHERE token_address = ?', (token_address,))
    row = c.fetchone()
    conn.close()
    if row:
        return {"token_address": row[1], "name": row[2], "liquidity": row[3], 
                "volume": row[4], "timestamp": row[5], "entry_price": row[6]}
    return None
