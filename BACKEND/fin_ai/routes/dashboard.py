from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User
from ..core.security import get_current_user
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

# Get dashboard statistics
@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get key dashboard statistics"""
    return {
        "marketSentiment": "Bullish",
        "aiPrediction": "Uptrend",
        "portfolioRisk": "Moderate",
        "aiConfidence": 82,
        "lastUpdated": datetime.utcnow().isoformat()
    }

# Get portfolio performance data
@router.get("/performance")
def get_performance_data(db: Session = Depends(get_db)):
    """Get portfolio performance over time"""
    base_value = 20000
    data = []
    for i in range(6):
        date = (datetime.utcnow() - timedelta(days=30-i*5)).strftime("%b %d")
        value = base_value + (i * 1000) + (500 if i % 2 == 0 else -300)
        data.append({"date": date, "value": value})
    return data

# Get market sentiment data
@router.get("/sentiment")
def get_sentiment_data(db: Session = Depends(get_db)):
    """Get market sentiment trends"""
    return [
        {"week": "Week 1", "positive": 18, "negative": 10},
        {"week": "Week 2", "positive": 22, "negative": 5},
        {"week": "Week 3", "positive": 25, "negative": 8},
        {"week": "Week 4", "positive": 28, "negative": 5},
    ]

# Get AI insight about dashboard
@router.get("/insight")
def get_dashboard_insight(db: Session = Depends(get_db)):
    """Get AI-generated insight for the dashboard"""
    return "Your portfolio is well-diversified with strong growth in tech and healthcare sectors. Market sentiment is bullish for Q2. Consider taking profits on top performers."

# Get quick stats summary
@router.get("/summary")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get summary of key metrics"""
    return {
        "portfolioValue": 22500,
        "dayGain": 350,
        "dayGainPercent": 1.58,
        "monthGain": 2500,
        "monthGainPercent": 12.5,
        "yearGain": 5500,
        "yearGainPercent": 32.4,
        "lastUpdated": datetime.utcnow().isoformat()
    }
