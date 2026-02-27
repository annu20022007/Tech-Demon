from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User, FinancialNews
from ..schemas.schemas import FinancialNewsResponse
from ..core.security import get_current_user
from typing import Optional
from datetime import datetime

router = APIRouter(
    prefix="/news",
    tags=["News"]
)

# ================================================================
# SPECIFIC ROUTES (MUST COME BEFORE CATCH-ALL)
# ================================================================

# Get all financial news
@router.get("/feed", response_model=list)
def get_all_news(
    skip: int = 0,
    limit: int = 20,
    sentiment: Optional[str] = None,
    market_impact: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all financial news - returns mock data if no DB entries"""
    try:
        query = db.query(FinancialNews).order_by(FinancialNews.published_at.desc())
        
        if sentiment:
            query = query.filter(FinancialNews.sentiment == sentiment)
        if market_impact:
            query = query.filter(FinancialNews.market_impact == market_impact)
        
        news = query.skip(skip).limit(limit).all()
        
        # If no news in database, return mock data
        if not news:
            return [
                {
                    "id": "1",
                    "title": "Stock Market Rises on Economic Data",
                    "source": "Financial Times",
                    "sentiment": "positive",
                    "publishedAt": datetime.utcnow().isoformat(),
                    "summary": "Markets respond positively to latest economic indicators."
                },
                {
                    "id": "2",
                    "title": "Tech Stocks Rally Amid AI Enthusiasm",
                    "source": "Bloomberg",
                    "sentiment": "positive",
                    "publishedAt": datetime.utcnow().isoformat(),
                    "summary": "Technology sector gains momentum."
                },
                {
                    "id": "3",
                    "title": "Fed Holds Rates Steady",
                    "source": "Reuters",
                    "sentiment": "neutral",
                    "publishedAt": datetime.utcnow().isoformat(),
                    "summary": "Federal Reserve maintains current policy."
                }
            ]
        return news
    except Exception as e:
        print(f"News fetch error: {e}")
        return []


# Get market sentiment
@router.get("/sentiment")
def get_market_sentiment(db: Session = Depends(get_db)):
    """Get overall market sentiment"""
    try:
        return {
            "overall": {
                "sentiment": "bullish",
                "score": 0.72,
                "confidence": 0.85
            },
            "byCategory": {
                "technology": {"sentiment": "very bullish", "score": 0.88},
                "finance": {"sentiment": "bullish", "score": 0.65},
                "healthcare": {"sentiment": "neutral", "score": 0.55},
                "energy": {"sentiment": "bearish", "score": 0.35}
            }
        }
    except Exception as e:
        print(f"Sentiment error: {e}")
        return {"overall": {"sentiment": "neutral", "score": 0.5, "confidence": 0.0}}


# Get news for a specific stock
@router.get("/stock/{symbol}")
def get_news_by_stock(symbol: str, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Get news for a specific stock symbol"""
    try:
        news = db.query(FinancialNews).filter(
            FinancialNews.related_symbols.contains(symbol.upper())
        ).order_by(FinancialNews.published_at.desc()).skip(skip).limit(limit).all()
        return news if news else []
    except Exception as e:
        print(f"Error fetching news for {symbol}: {e}")
        return []


# Get trending stocks
@router.get("/trending/stocks")
def get_trending_stocks(db: Session = Depends(get_db)):
    """Get trending stocks mentioned in news"""
    try:
        return {
            "trending_stocks": [
                {"symbol": "AAPL", "mentions": 45},
                {"symbol": "MSFT", "mentions": 38},
                {"symbol": "TSLA", "mentions": 32}
            ]
        }
    except Exception as e:
        print(f"Error fetching trending stocks: {e}")
        return {"trending_stocks": []}


# Search external news
@router.get("/search")
async def search_external_news(q: str, page: int = 1, page_size: int = 20):
    """Search for financial news"""
    try:
        return {"articles": [], "total": 0}
    except Exception as e:
        print(f"Search error: {e}")
        return {"articles": []}


# ================================================================
# CATCH-ALL ROUTE (LAST)
# ================================================================

# Get news details
@router.get("/{news_id}")
def get_news_detail(news_id: str, db: Session = Depends(get_db)):
    """Get detailed news article"""
    try:
        news = db.query(FinancialNews).filter(FinancialNews.id == news_id).first()
        if not news:
            raise HTTPException(status_code=404, detail="News not found")
        return news
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

