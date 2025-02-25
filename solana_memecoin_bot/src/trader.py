import asyncio
from telethon import TelegramClient
import logging
from src.database import update_entry_price, get_coin
from src.config import load_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def execute_trade(token_address, action, amount_sol, client, config):
    """Execute a trade via Toxi Bot using Telethon."""
    chat_id = config["telegram"]["chat_id"]
    if action == "buy":
        message = f"/buy {token_address} {amount_sol} SOL --slippage {config['trading']['slippage']} --priority high"
    elif action == "sell":
        message = f"/sell {token_address} --slippage {config['trading']['slippage']} --priority high"
    await client.send_message(chat_id, message)
    logger.info(f"Executed {action} for {token_address} with {amount_sol if amount_sol else 'all'} SOL")

async def trade_logic(token_address, current_price, client, config):
    """Determine and execute buy/sell trades."""
    coin = get_coin(token_address)
    entry_price = coin.get("entry_price") if coin else None

    if entry_price is None:
        amount_sol = min(max(config["trading"]["min_buy_sol"], 
                            config["trading"]["max_buy_sol"] * (current_price / 1000)), 
                        config["trading"]["max_buy_sol"])
        await execute_trade(token_address, "buy", amount_sol, client, config)
        update_entry_price(token_address, current_price)
        return True
    elif current_price >= entry_price * config["trading"]["profit_target"]:
        await execute_trade(token_address, "sell", None, client, config)
        update_entry_price(token_address, None)
        return True
    return False

# Example usage (integrate into main.py)
async def main():
    config = load_config()
    client = TelegramClient('bot_session', config["telegram"]["api_id"], config["telegram"]["api_hash"])
    await client.start(phone=config["telegram"]["phone_number"])
    # Proceed with trading logic
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
