from fastapi import APIRouter, Depends, Query
from app.services.coingecko import get_markets
from app.models.schemas import MarketData

router = APIRouter(prefix="/api/v3", tags=["markets"])

@router.get("/coins/markets", response_model=list[MarketData])
async def get_coins_markets(
    vs_currency: str = "usd",
    order: str = "market_cap_desc",
    per_page: int = 50,
    page: int = 1,
    sparkline: bool = False,
    data: list = Depends(get_markets)
):
    return data