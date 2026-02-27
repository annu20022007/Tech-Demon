import httpx
from fin_ai.core import config

NEWSAPI_URL = "https://newsapi.org/v2/everything"

async def search_news(query: str, page: int = 1, page_size: int = 20):
    if config.NEWSAPI_KEY:
        params = {
            "q": query,
            "page": page,
            "pageSize": page_size,
            "apiKey": config.NEWSAPI_KEY,
        }
        async with httpx.AsyncClient() as client:
            r = await client.get(NEWSAPI_URL, params=params)
            r.raise_for_status()
            return r.json()
    elif config.FINNHUB_API_KEY:
        # Finnhub implementation could go here
        raise NotImplementedError("Finnhub support not yet implemented")
    else:
        raise RuntimeError("No news API key configured")
