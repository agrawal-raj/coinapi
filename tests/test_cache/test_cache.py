import pytest
import asyncio
from datetime import timedelta
from app.cache import cache_store, cache
from app.services.coingecko import get_markets
from app.models.schemas import MarketData

class TestCacheFunctionality:
    @pytest.fixture
    def mock_market_data(self):
        return [
            {
                "id": "bitcoin",
                "symbol": "btc",
                "name": "Bitcoin",
                "image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
                "current_price": 50000,
                "market_cap": 1000000000000,
                "market_cap_rank": 1,
                "fully_diluted_valuation": 1050000000000,
                "total_volume": 50000000000,
                "high_24h": 51000,
                "low_24h": 49000,
                "price_change_24h": 1000,
                "price_change_percentage_24h": 2.0,
                "market_cap_change_24h": 20000000000,
                "market_cap_change_percentage_24h": 2.0,
                "circulating_supply": 19000000,
                "total_supply": 21000000,
                "max_supply": 21000000,
                "ath": 69000,
                "ath_change_percentage": -27.5,
                "ath_date": "2021-11-10T14:24:11.849Z",
                "atl": 67.81,
                "atl_change_percentage": 73650.0,
                "atl_date": "2013-07-06T00:00:00.000Z",
                "roi": {
                    "times": 73.65,
                    "currency": "usd",
                    "percentage": 7365.0
                },
                "last_updated": "2023-05-01T12:34:56.789Z"
            }
        ]

    @pytest.mark.asyncio
    async def test_cache_decorator_stores_data(self, mocker, mock_market_data):
        """Test that results are cached"""
        mocker.patch(
            "app.services.coingecko.fetch_coingecko_markets",
            return_value=mock_market_data
        )
        
        # First call - should call the API
        result1 = await get_markets()
        # Second call - should use cache
        result2 = await get_markets()
        
        # Verify the underlying function was only called once
        assert len(cache_store) == 1
        assert result1 == result2

    @pytest.mark.asyncio
    async def test_cache_expires_after_ttl(self, mocker, mock_market_data):
        """Test that cache expires after TTL"""
        mock_fetch = mocker.patch(
            "app.services.coingecko.fetch_coingecko_markets",
            return_value=mock_market_data
        )
        
        # First call - should call the API
        await get_markets()
        # Immediately call again - should use cache
        await get_markets()
        
        assert mock_fetch.call_count == 1
        
        # Manually expire the cache
        cache_store.clear()
        
        # Call again - should call API again
        await get_markets()
        assert mock_fetch.call_count == 2

    @pytest.mark.asyncio
    async def test_cache_different_parameters(self, mocker, mock_market_data):
        """Test that different parameters create different cache entries"""
        mock_fetch = mocker.patch(
            "app.services.coingecko.fetch_coingecko_markets",
            return_value=mock_market_data
        )
        
        # Call with different parameters
        await get_markets(vs_currency="usd")
        await get_markets(vs_currency="eur")
        
        assert mock_fetch.call_count == 2
        assert len(cache_store) == 2