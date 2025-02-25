import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from src.trader import send_telegram_message, execute_trade, trade_logic

@pytest.fixture
def mock_config():
    return {
        "telegram": {"bot_token": "test_token", "chat_id": "test_chat"},
        "trading": {"min_buy_sol": 0.01, "max_buy_sol": 0.15, "slippage": 30, "profit_target": 10}
    }

@pytest.mark.asyncio
async def test_send_telegram_message(mock_config):
    """Test sending a Telegram message."""
    bot = AsyncMock()
    bot.send_message = AsyncMock()
    await send_telegram_message(bot, mock_config, "/buy TEST123 0.05 SOL")
    bot.send_message.assert_called_with(chat_id="test_chat", text="/buy TEST123 0.05 SOL")

@pytest.mark.asyncio
async def test_execute_trade_buy(mock_config):
    """Test executing a buy trade."""
    with patch("telegram.Bot", return_value=AsyncMock()) as mock_bot:
        mock_bot.return_value.send_message = AsyncMock()
        await execute_trade("TEST123", "buy", 0.05, mock_config)
        mock_bot.return_value.send_message.assert_called_with(chat_id="test_chat", 
                                                              text="/buy TEST123 0.05 SOL --slippage 30 --priority high")

@pytest.mark.asyncio
async def test_trade_logic_buy(mock_config):
    """Test trade logic for buying."""
    with patch("src.trader.get_coin", return_value=None):
        with patch("src.trader.execute_trade", new_callable=AsyncMock) as mock_execute:
            with patch("src.trader.update_entry_price") as mock_update:
                result = await trade_logic("TEST123", 0.1, mock_config)
                assert result is True
                mock_execute.assert_called_once()
                mock_update.assert_called_with("TEST123", 0.1)

@pytest.mark.asyncio
async def test_trade_logic_sell(mock_config):
    """Test trade logic for selling at 10x profit."""
    with patch("src.trader.get_coin", return_value={"entry_price": 0.1}):
        with patch("src.trader.execute_trade", new_callable=AsyncMock) as mock_execute:
            with patch("src.trader.update_entry_price") as mock_update:
                result = await trade_logic("TEST123", 1.0, mock_config)  # 10x from 0.1
                assert result is True
                mock_execute.assert_called_with("TEST123", "sell", None, mock_config)
                mock_update.assert_called_with("TEST123", None)
