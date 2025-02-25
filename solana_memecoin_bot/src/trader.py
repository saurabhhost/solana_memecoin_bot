import telegram
import asyncio
import logging
from src.database import update_entry_price, get_coin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def send_telegram_message(bot, config, message):
    """Send a message to Toxi Bot via Telegram."""
    await bot.send_message(chat_id=config["telegram"]["chat_id"], text=message)

async def execute_trade(token_address, action, amount_sol, config):
    """Execute a buy or sell trade via Toxi Bot."""
    bot = telegram.Bot(token=config["telegram"]["bot_token"])
    if action == "buy":
        message = f"/buy {token_address} {amount_sol} SOL --slippage {config['trading']['slippage']} --priority high"
    elif action == "sell":
        message = f"/sell {token_address} --slippage {config['trading']['slippage']} --priority high"
    await send_telegram_message(bot, config, message)
    logger.info(f"Executed {action} for {token_address} with {amount_sol if amount_sol else 'all'} SOL")

async def trade_logic(token_address, current_price, config):
    """Determine and execute buy/sell trades."""
    coin = get_coin(token_address)
    entry_price = coin.get("entry_price") if coin else None

    if entry_price is None:  # Buy condition
        amount_sol = min(max(config["trading"]["min_buy_sol"], 
                            config["trading"]["max_buy_sol"] * (current_price / 1000)), 
                        config["trading"]["max_buy_sol"])
        await execute_trade(token_address, "buy", amount_sol, config)
        entry_price = current_price
        update_entry_price(token_address, entry_price)
        return True
    elif current_price >= entry_price * config["trading"]["profit_target"]:  # Sell at 10x
        await execute_trade(token_address, "sell", None, config)
        update_entry_price(token_address, None)  # Reset
        return True
    return False
