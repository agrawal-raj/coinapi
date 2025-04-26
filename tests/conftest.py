import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def mock_coingecko_response():
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

@pytest.fixture
def mock_market_data(mock_coingecko_response):
    from app.models.schemas import MarketData
    return [MarketData(**item) for item in mock_coingecko_response]