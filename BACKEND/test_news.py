import asyncio
from fin_ai.clients.news_client import search_news

async def main():
    try:
        res = await search_news('Apple', page=1)
        print('news ok', list(res.keys()))
    except Exception as e:
        print('news error', e)

asyncio.run(main())
