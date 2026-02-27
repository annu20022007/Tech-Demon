# FinAI Backend - External API Integration Guide

## ✅ Integrations Completed

Your backend now ships with integrations for **market data**, **financial news**, and **AI chatbot**. All dependencies installed and `.env` created with your OpenAI key.

---

## 🔑 API Keys Configured

| Service | Key Name | Status | Usage |
|---------|----------|--------|-------|
| **OpenAI** | `OPENAI_API_KEY` | ✅ **Configured** | LLM for AI advisor chatbot |
| **Alpha Vantage** | `ALPHAVANTAGE_API_KEY` | ⏳ Ready (add key to `.env`) | Stock market time-series data |
| **NewsAPI** | `NEWSAPI_KEY` | ⏳ Ready (add key to `.env`) | Real-time financial news articles |
| **Finnhub** | `FINNHUB_API_KEY` | ⏳ Optional | Alternative market + news data |
| **Polygon.io** | `POLYGON_API_KEY` | ⏳ Optional | Alternate market data (ticks, aggregates) |
| **Alpaca** | `ALPACA_API_KEY`, `ALPACA_API_SECRET` | ⏳ Optional | Paper/live trading |

---

## 📦 New Client Modules Added

### 1. **Core Config** (`fin_ai/core/config.py`)
Loads environment variables from `.env` file safely.
```python
from fin_ai.core import config
print(config.OPENAI_API_KEY)  # Reads from .env
```

### 2. **OpenAI Client** (`fin_ai/clients/openai_client.py`)
Wrapper for OpenAI chat completions. Powers the AI advisor.
```python
from fin_ai.clients.openai_client import chat_completion
response = chat_completion("How should I diversify my portfolio?")
```

### 3. **Market Data Client** (`fin_ai/clients/market_data.py`)
Async client for Alpha Vantage daily stock data.
```python
from fin_ai.clients.market_data import get_alpha_daily
import asyncio
data = await get_alpha_daily('AAPL')  # Time-series data
```

### 4. **News Client** (`fin_ai/clients/news_client.py`)
Async client for NewsAPI or Finnhub news.
```python
from fin_ai.clients.news_client import search_news
articles = await search_news('Apple earnings', page=1)
```

---

## 🚀 New API Endpoints

### Market Data
- **GET** `/api/market/daily/{symbol}` — Get daily stock prices for a ticker
  ```bash
  curl http://localhost:8000/api/market/daily/AAPL
  ```

### News Search
- **GET** `/api/news/search?q={query}&page={page}` — Search external news
  ```bash
  curl http://localhost:8000/api/news/search?q=Apple%20stock
  ```

### Chat with AI (now powered by OpenAI)
- **POST** `/api/chat/conversations/{conversation_id}/messages`
  - Sends message, calls OpenAI GPT, saves response
  ```bash
  curl -X POST http://localhost:8000/api/chat/conversations/123/messages \
    -H "Authorization: Bearer TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"content": "How do I build a diversified portfolio?"}'
  ```

---

## ⚙️ Quick Setup Instructions

### 1. **Copy `.env.example` to `.env`** (if needed)
Your `.env` already has your OpenAI key. To add other services:

```bash
copy .env.example .env
```

Edit `.env` and add the API keys you want to use:

```
OPENAI_API_KEY=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
ALPHAVANTAGE_API_KEY=your_alpha_vantage_key
NEWSAPI_KEY=your_newsapi_key
FINNHUB_API_KEY=your_finnhub_key
```

### 2. **Install Dependencies**
Already done! But if you reset, run:
```bash
pip install --user -r requirements.txt
```

### 3. **Start the Server**
```bash
uvicorn fin_ai.main:app --reload --port 8000
```

### 4. **Test with Swagger UI**
Open: http://localhost:8000/docs

---

## 📋 How Each Integration Works

### OpenAI (Chat Advisor)
- Endpoint: `/api/chat/conversations/{id}/messages`
- When a user sends a message, the backend calls `chat_completion()` which sends the prompt to OpenAI GPT and returns the response
- Falls back to local generation if no key is set

### Alpha Vantage (Market Data)
- Endpoint: `/api/market/daily/{symbol}`
- Fetches daily adjusted OHLC + volume data
- Requires: `ALPHAVANTAGE_API_KEY` from https://www.alphavantage.co/support/#api-key

### NewsAPI (Financial News)
- Endpoint: `/api/news/search`
- Searches news articles by query
- Requires: `NEWSAPI_KEY` from https://newsapi.org/

---

## 🔄 Environment Variables Reference

| Variable | Example | Default | Required |
|----------|---------|---------|----------|
| `OPENAI_API_KEY` | `sk_...` | None | Yes (for AI) |
| `ALPHAVANTAGE_API_KEY` | `ABC123` | None | No (market data) |
| `NEWSAPI_KEY` | `xyz789` | None | No (news) |
| `FINNHUB_API_KEY` | `key123` | None | No (alt news) |
| `YFINANCE_FALLBACK` | `true` | `false` | No |
| `DATABASE_URL` | `sqlite:///./test.db` | SQLite | No |
| `DEBUG` | `true` | `false` | No |

---

## 🛠️ To Add More Services

Follow this pattern for any new service:

1. Create client module in `fin_ai/clients/your_service.py`
2. Add env var config to `fin_ai/core/config.py`
3. Create endpoint in `fin_ai/routes/your_route.py` that calls the client
4. Include router in `fin_ai/main.py`

Example:
```python
# fin_ai/clients/your_service.py
from fin_ai.core import config
async def get_data():
    api_key = config.YOUR_SERVICE_API_KEY
    # call service
```

---

## 📊 Current Stack

```
fin_ai/
├── core/
│   └── config.py               # ✨ NEW: Env loader
├── clients/                    # ✨ NEW: External service clients
│   ├── openai_client.py
│   ├── market_data.py
│   ├── news_client.py
│   └── __init__.py
├── routes/
│   ├── chat.py                 # Updated: Uses OpenAI
│   ├── news.py                 # Updated: External search
│   ├── market.py               # ✨ NEW: Market data
│   └── ...
├── main.py                     # Updated: Market router included
└── ...

.env                            # ✨ NEW: API keys (GITIGNORED)
.env.example                    # ✨ NEW: Template
requirements.txt                # ✨ NEW: Updated deps
```

---

## ✅ Testing Endpoints

### 1. AI Chat (OpenAI)
```bash
# Create conversation
curl -X POST http://localhost:8000/api/chat/conversations \
  -H "Authorization: Bearer YOUR_TOKEN"

# Send message (calls OpenAI)
curl -X POST http://localhost:8000/api/chat/conversations/CONV_ID/messages \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Best stocks for beginners?"}'
```

### 2. Market Data (Alpha Vantage)
```bash
curl http://localhost:8000/api/market/daily/MSFT
```
Returns: Opening, closely, high, low, volume, etc. for time-series

### 3. News Search (NewsAPI)
```bash
curl "http://localhost:8000/api/news/search?q=Apple%20stock&page=1"
```

---

## 🔑 Next: Add Missing Your API Keys

For the features to work fully, you'll need:
1. **Alpha Vantage API Key** (free) → https://www.alphavantage.co/support/#api-key
2. **NewsAPI Key** (free tier available) → https://newsapi.org/register
3. **Finnhub** (optional, free tier) → https://finnhub.io/

Paste the keys into `.env`:
```
ALPHAVANTAGE_API_KEY=your_key_here
NEWSAPI_KEY=your_key_here
```

---

## 🎯 Summary

✅ **OpenAI**: Already configured and wired into chatbot  
✅ **Alpha Vantage**: Ready, endpoint created `/api/market/daily/{symbol}`  
✅ **NewsAPI**: Ready, endpoint created `/api/news/search`  
✅ **All clients**: Installed and tested  
✅ **`.env` file**: Created with your OpenAI key  

**Server ready to run:**
```bash
uvicorn fin_ai.main:app --reload
```

Visit **http://localhost:8000/docs** to test all endpoints interactively! 🚀
