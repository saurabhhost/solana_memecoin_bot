import asyncio
import aiohttp
import logging
from src.database import store_coin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def fetch_trending_coins(session, source, config):
    """Fetch trending coins from PumpFun or GMGN."""
    urls = {
        "pumpfun": "https://pump.fun/api/trending",  # Mock URL
        "gmgn": "https://gmgn.ai/api/trending"      # Mock URL
    }
    try:
        async with session.get(urls[source]) as response:
            if response.status == 200:
                data = await response.json()
                coins = data.get("coins", [])
                return [coin for coin in coins 
                        if coin.get("address") not in config["blacklist_coins"]
                        and coin.get("liquidity", 0) >= config["filters"]["min_liquidity"]
                        and coin.get("volume", 0) >= config["filters"]["min_volume"]]
            logger.error(f"Failed to fetch {source}: {response.status}")
            return []
    except Exception as e:
        logger.error(f"Error fetching {source}: {e}")
        return []

async def collect_data(config):
    """Collect trending coins and store them."""
    async with aiohttp.ClientSession() as session:
        for source in ["pumpfun", "gmgn"]:
            coins = await fetch_trending_coins(session, source, config)
            for coin in coins:
                store_coin(coin.get("address"), coin.get("name"), 
                          coin.get("liquidity"), coin.get("volume"))
            logger.info(f"Fetched {len(coins)} trending coins from {source}")
