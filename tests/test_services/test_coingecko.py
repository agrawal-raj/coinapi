import pytest
from unittest.mock import AsyncMock
from httpx import RequestError
from app.services.coingecko import fetch_coingecko_markets, get_markets
from app.models.schemas import MarketData

class TestCoinGeckoService:
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
    async def test_fetch_coingecko_markets_success(self, mocker, mock_market_data):
        """Test successful API call to CoinGecko"""
        mock_client = AsyncMock()
        mock_client.get.return_value.status_code = 200
        mock_client.get.return_value.json.return_value = mock_market_data
        mocker.patch("httpx.AsyncClient", return_value=mock_client)
        
        result = await fetch_coingecko_markets()
        assert isinstance(result, list)
        assert result[0]["id"] == "bitcoin"

    @pytest.mark.asyncio
    async def test_fetch_coingecko_markets_failure(self, mocker):
        """Test failed API call to CoinGecko"""
        mock_client = AsyncMock()
        mock_client.get.return_value.raise_for_status.side_effect = RequestError("API error")
        mocker.patch("httpx.AsyncClient", return_value=mock_client)
        
        with pytest.raises(RequestError):
            await fetch_coingecko_markets()

    @pytest.mark.asyncio
    async def test_get_markets_returns_valid_schema(self, mocker, mock_market_data):
        """Test get_markets returns properly formatted data"""
        mocker.patch(
            "app.services.coingecko.fetch_coingecko_markets",
            return_value=mock_market_data
        )
        
        result = await get_markets()
        assert isinstance(result, list)
        assert isinstance(result[0], MarketData)