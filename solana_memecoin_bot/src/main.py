import asyncio
import aiohttp
import logging
from src.config import load_config
from src.database import init_db
from src.data_collector import collect_data
from src.safety_checker import is_safe_token
from src.social_analyzer import analyze_social_activity
from src.trader import trade_logic

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def process_coin(session, coin, config):
    """Process a single coin through safety, social, and trading checks."""
    token_address = coin["address"]
    
    if not is_safe_token(token_address, config):
        logger.info(f"{token_address} failed safety check")
        return None
    
    if analyze_social_activity(token_address) < 1:
        logger.info(f"{token_address} lacks influencer support")
        return None
    
    # Mock price (replace with real price feed)
    current_price = coin.get("price", 1.0)
    if await trade_logic(token_address, current_price, config):
        return token_address
    return None

async def main():
    """Main loop for the trading bot."""
    config = load_config()
    init_db()
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                await collect_data(config)
                conn = sqlite3.connect('memecoins.db')
                c = conn.cursor()
                c.execute("SELECT token_address, name, liquidity, volume FROM coins")
                coins = [{"address": row[0], "name": row[1], "liquidity": row[2], "volume": row[3]} 
                         for row in c.fetchall()]
                conn.close()
                
                for coin in coins:
                    result = await process_coin(session, coin, config)
                    if result:
                        logger.info(f"Processed {result} successfully")
                await asyncio.sleep(60)
            except Exception as e:
                logger.error(f"Main loop error: {e}")
                await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
