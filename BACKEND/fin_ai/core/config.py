import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
# Determine project root (two levels up from this file)
project_root = Path(__file__).parent.parent.parent
# also allow .env in current working directory
env_path = project_root / ".env"
if not env_path.exists():
    env_path = Path.cwd() / ".env"
if env_path.exists():
    load_dotenv(env_path)

# API keys and settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
IEX_CLOUD_API_KEY = os.getenv("IEX_CLOUD_API_KEY")
YFINANCE_FALLBACK = os.getenv("YFINANCE_FALLBACK", "false").lower() == "true"
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_API_SECRET = os.getenv("ALPACA_API_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Other config
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# For convenience, you can add more settings here as needed
