from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User
from ..core.security import get_current_user
from datetime import datetime

router = APIRouter(
    prefix="/advisor",
    tags=["AI Advisor"]
)


@router.post("/recommendations")
async def get_recommendations(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get personalized financial recommendations based on user profile"""
    portfolio_value = data.get("portfolioValue", 50000)
    risk_tolerance = data.get("riskTolerance", "moderate")
    investment_horizon = data.get("investmentHorizon", 5)
    
    # Generate personalized recommendations
    recommendations = []
    
    if risk_tolerance == "conservative":
        recommendations = [
            {
                "id": "rec_001",
                "title": "Increase Bond Allocation",
                "description": "With your conservative risk profile, consider allocating 60-70% to bonds and fixed income",
                "impact": "Reduces volatility, provides stable income",
                "confidence": 0.92,
                "action": "Rebalance portfolio to 65% bonds, 25% stocks, 10% cash"
            },
            {
                "id": "rec_002",
                "title": "Dividend-Paying Stocks",
                "description": "Focus on blue-chip stocks with consistent dividend history for steady income",
                "impact": "Provides regular income with lower volatility",
                "confidence": 0.88,
                "action": "Allocate $5000 to dividend aristocrats (JNJ, PG, KO)"
            }
        ]
    elif risk_tolerance == "moderate":
        recommendations = [
            {
                "id": "rec_001",
                "title": "Balanced Portfolio Growth",
                "description": "Maintain a balanced 50/50 split between equities and fixed income for steady growth",
                "impact": "Balanced risk-return profile",
                "confidence": 0.90,
                "action": "Rebalance to 50% stocks, 40% bonds, 10% alternatives"
            },
            {
                "id": "rec_002",
                "title": "Add Tech Exposure",
                "description": "Include growth-oriented tech stocks (5-10% of portfolio) for upside potential",
                "impact": "Higher growth potential with moderate risk",
                "confidence": 0.85,
                "action": "Allocate $3000-5000 to diversified tech ETF (QQQ)"
            },
            {
                "id": "rec_003",
                "title": "Diversify into Sectors",
                "description": "Spread investments across healthcare, technology, financials, and consumer sectors",
                "impact": "Reduces concentration risk",
                "confidence": 0.87,
                "action": "Use sector-specific ETFs for diversification"
            }
        ]
    else:  # aggressive
        recommendations = [
            {
                "id": "rec_001",
                "title": "Growth Stock Focus",
                "description": "Allocate 70-80% to growth stocks and emerging markets for maximum appreciation",
                "impact": "High potential returns, higher volatility",
                "confidence": 0.88,
                "action": "Invest in growth ETFs (QQQ, VUG) and emerging market funds"
            },
            {
                "id": "rec_002",
                "title": "Options Trading Strategy",
                "description": "Use covered calls on held positions to generate additional income",
                "impact": "Generate yield while maintaining upside",
                "confidence": 0.82,
                "action": "Sell covered calls on 20-30% of stock holdings"
            },
            {
                "id": "rec_003",
                "title": "Leverage for Amplified Returns",
                "description": "Consider using margin carefully for positions you're highly confident in",
                "impact": "Amplify returns (and losses), requires discipline",
                "confidence": 0.75,
                "action": "Use margin conservatively (max 10% of capital)"
            }
        ]
    
    return {
        "status": "success",
        "recommendations": recommendations,
        "summary": f"Generated {len(recommendations)} recommendations for {risk_tolerance} portfolio",
        "lastUpdated": datetime.utcnow().isoformat()
    }


@router.post("/chat")
async def advisor_chat(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Chat with AI financial advisor about investment questions"""
    message = data.get("message", "")
    context = data.get("context", {})
    
    # Mock responses based on different question types
    responses = {
        "market": "The current market shows mixed signals. Tech is up 2.3% while financials are down 1.5%. Volatility remains elevated at 18 VIX. Consider diversifying across sectors.",
        "portfolio": "Your portfolio allocation looks good. With $50k invested, you have healthy diversification. Consider rebalancing if any position exceeds 20% of your total.",
        "risk": "Risk tolerance is personal. Conservative investors should focus on bonds and dividend stocks. Moderate investors can balance growth and income. Aggressive investors can pursue growth opportunities.",
        "trading": "Remember: only invest what you can afford to lose. Do thorough research before buying. Diversification is key. Don't try to time the market - use dollar-cost averaging instead.",
        "default": "That's a great question! Based on current market conditions and your profile, I'd recommend: 1) Diversify your holdings, 2) Focus on quality companies, 3) Have a long-term perspective. What specific area interests you?"
    }
    
    # Determine response type
    message_lower = message.lower()
    if any(word in message_lower for word in ["market", "trend", "index", "performance"]):
        response = responses["market"]
    elif any(word in message_lower for word in ["portfolio", "allocation", "rebalance"]):
        response = responses["portfolio"]
    elif any(word in message_lower for word in ["risk", "safe", "aggressive", "conservative"]):
        response = responses["risk"]
    elif any(word in message_lower for word in ["trade", "buy", "sell", "swing"]):
        response = responses["trading"]
    else:
        response = responses["default"]
    
    return {
        "status": "success",
        "response": response,
        "timestamp": datetime.utcnow().isoformat(),
        "conversationId": f"conv_{datetime.utcnow().timestamp().__str__()}"
    }


@router.post("/portfolio-analysis")
async def analyze_portfolio(
    data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze user's portfolio for strengths and weaknesses"""
    holdings = data.get("holdings", [])
    total_value = data.get("totalValue", 50000)
    
    analysis = {
        "strengthAreas": [
            {
                "area": "Diversification",
                "score": 8,
                "description": "Good spread across sectors and asset classes",
                "suggestion": "Maintain current diversification strategy"
            },
            {
                "area": "Growth Potential",
                "score": 7,
                "description": "15-20% of portfolio in growth stocks provides upside",
                "suggestion": "Consider increasing to 20-25% for more growth"
            }
        ],
        "weakAreas": [
            {
                "area": "Income Generation",
                "score": 5,
                "description": "Limited dividend-paying positions",
                "suggestion": "Add 3-5 dividend aristocrats for steady income"
            },
            {
                "area": "Risk Management",
                "score": 6,
                "description": "Moderate hedging in place",
                "suggestion": "Consider adding 10% bonds for downside protection"
            }
        ],
        "overallScore": 7,
        "recommendation": "Your portfolio is well-balanced. Focus on income generation and risk management.",
        "allocations": {
            "stocks": {
                "percentage": 60,
                "value": total_value * 0.6,
                "status": "healthy"
            },
            "bonds": {
                "percentage": 30,
                "value": total_value * 0.3,
                "status": "good"
            },
            "cash": {
                "percentage": 10,
                "value": total_value * 0.1,
                "status": "adequate"
            }
        }
    }
    
    return {
        "status": "success",
        "analysis": analysis,
        "lastAnalyzed": datetime.utcnow().isoformat()
    }
