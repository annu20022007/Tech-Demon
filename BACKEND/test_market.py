import asyncio
from fin_ai.clients.market_data import get_alpha_daily

async def test():
    try:
        data = await get_alpha_daily('MSFT')
        print('market client ok', list(data.keys())[:3])
    except Exception as e:
        print('market client error', e)

asyncio.run(test())
