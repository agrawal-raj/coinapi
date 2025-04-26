import os
from typing import Optional
import httpx
from app.cache import cache
from app.models.schemas import MarketData
from fastapi import HTTPException

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

async def fetch_coingecko_markets(
    vs_currency: str = "usd",
    order: str = "market_cap_desc",
    per_page: int = 50,
    page: int = 1,
    sparkline: bool = False
) -> list[dict]:
    params = {
        "vs_currency": vs_currency,
        "order": order,
        "per_page": per_page,
        "page": page,
        "sparkline": str(sparkline).lower()
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{COINGECKO_API_URL}/coins/markets",
                params=params,
                timeout=10.0
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail="Error fetching data from CoinGecko API"
            )

@cache(ttl=300)  # Cache for 5 minutes
async def get_markets(
    vs_currency: str = "usd",
    order: str = "market_cap_desc",
    per_page: int = 50,
    page: int = 1,
    sparkline: bool = False
) -> list[MarketData]:
    data = await fetch_coingecko_markets(
        vs_currency=vs_currency,
        order=order,
        per_page=per_page,
        page=page,
        sparkline=sparkline
    )
    return [MarketData(**item) for item in data]