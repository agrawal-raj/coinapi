import pytest
from fastapi import status
from app.models.schemas import MarketData

class TestMarketsRouter:
    def test_get_markets_success(self, client, mock_coingecko_response, mocker):
        """Test successful market data retrieval"""
        mocker.patch(
            "app.services.coingecko.get_markets",
            return_value=[MarketData(**item) for item in mock_coingecko_response]
        )
        
        response = client.get("/api/v3/coins/markets")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert data[0]["id"] == "bitcoin"

    def test_get_markets_with_params(self, client, mock_coingecko_response, mocker):
        """Test with query parameters"""
        mocker.patch(
            "app.services.coingecko.get_markets",
            return_value=[MarketData(**item) for item in mock_coingecko_response]
        )
        
        response = client.get(
            "/api/v3/coins/markets",
            params={"vs_currency": "eur", "per_page": 5}
        )
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1  # Our mock returns 1 item

    def test_get_markets_validation_error(self, client):
        """Test invalid parameter values"""
        response = client.get(
            "/api/v3/coins/markets",
            params={"per_page": 251}  # Above maximum allowed
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY