import httpx
from fin_ai.core import config

BASE_URL_ALPHA = "https://www.alphavantage.co/query"

async def get_alpha_daily(symbol: str):
    if not config.ALPHAVANTAGE_API_KEY:
        raise RuntimeError("Alpha Vantage API key not configured")
    params = {
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": config.ALPHAVANTAGE_API_KEY,
    }
    async with httpx.AsyncClient() as client:
        r = await client.get(BASE_URL_ALPHA, params=params)
        r.raise_for_status()
        return r.json()

# yfinance fallback can be implemented later
