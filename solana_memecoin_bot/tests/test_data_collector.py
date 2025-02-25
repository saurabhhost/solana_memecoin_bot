import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from src.data_collector import fetch_trending_coins, collect_data

@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    return {
        "blacklist_coins": ["BLACK123"],
        "filters": {"min_liquidity": 1000, "min_volume": 5000}
    }

@pytest.mark.asyncio
async def test_fetch_trending_coins_success(mock_config):
    """Test fetching trending coins with a successful response."""
    mock_response = {
        "coins": [
            {"address": "COIN1", "name": "Coin1", "liquidity": 2000, "volume": 6000},
            {"address": "BLACK123", "name": "BlackCoin", "liquidity": 3000, "volume": 7000}
        ]
    }
    session = AsyncMock()
    session.get.return_value.__aenter__.return_value.status = 200
    session.get.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response)

    coins = await fetch_trending_coins(session, "pumpfun", mock_config)
    assert len(coins) == 1  # BLACK123 should be filtered out
    assert coins[0]["address"] == "COIN1"

@pytest.mark.asyncio
async def test_fetch_trending_coins_failure(mock_config):
    """Test fetching coins with a failed response."""
    session = AsyncMock()
    session.get.return_value.__aenter__.return_value.status = 404

    coins = await fetch_trending_coins(session, "gmgn", mock_config)
    assert coins == []

@pytest.mark.asyncio
async def test_collect_data(mock_config):
    """Test collect_data calls fetch_trending_coins."""
    with patch("src.data_collector.fetch_trending_coins", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = [{"address": "COIN1", "name": "Coin1", "liquidity": 2000, "volume": 6000}]
        with patch("src.data_collector.store_coin") as mock_store:
            await collect_data(mock_config)
            assert mock_fetch.call_count == 2  # Called for pumpfun and gmgn
            mock_store.assert_called_once()
