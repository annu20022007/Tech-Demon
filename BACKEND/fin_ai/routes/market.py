from fastapi import APIRouter, HTTPException
from fin_ai.clients.market_data import get_alpha_daily

router = APIRouter(
    prefix="/market",
    tags=["Market Data"]
)

@router.get("/daily/{symbol}")
async def daily_prices(symbol: str):
    try:
        data = await get_alpha_daily(symbol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return data
