from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User, Prediction, FinancialNews
from ..schemas.schemas import PredictionCreate, PredictionResponse, PredictionEvaluate
from ..core.security import get_current_user
from datetime import datetime
import httpx
import asyncio
from typing import Optional

router = APIRouter(
    prefix="/prediction",
    tags=["Predictions"]
)


async def fetch_news_for_stock(symbol: str) -> list:
    """Fetch recent news for a stock symbol using NewsAPI"""
    from fin_ai.core import config
    
    if not config.NEWSAPI_KEY:
        return []
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://newsapi.org/v2/everything",
                params={
                    "q": symbol,
                    "sortBy": "publishedAt",
                    "language": "en",
                    "pageSize": 10,
                    "apiKey": config.NEWSAPI_KEY
                },
                timeout=10.0
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("articles", [])
    except Exception as e:
        print(f"Error fetching news: {e}")
    
    return []


async def fetch_price_data(symbol: str) -> dict:
    """Fetch recent price data from Alpha Vantage"""
    from fin_ai.core import config
    
    if not config.ALPHAVANTAGE_API_KEY:
        return {"trend": "neutral", "recent_data": []}
    
    try:
        from alpha_vantage.timeseries import TimeSeries
        ts = TimeSeries(key=config.ALPHAVANTAGE_API_KEY, output_format='pandas')
        data, meta = ts.get_daily(symbol=symbol, outputsize='compact')
        
        if len(data) > 0:
            # Get last 5 days
            recent = data.head(5)
            closes = recent['4. close'].tolist()
            
            # Determine trend
            if len(closes) >= 2:
                if closes[0] > closes[-1]:
                    trend = "down"
                elif closes[0] < closes[-1]:
                    trend = "up"
                else:
                    trend = "neutral"
            else:
                trend = "neutral"
            
            return {
                "trend": trend,
                "recent_prices": closes,
                "latest_price": closes[0] if closes else None
            }
    except Exception as e:
        print(f"Error fetching price data: {e}")
    
    return {"trend": "neutral", "recent_prices": []}


def analyze_news_sentiment(articles: list, symbol: str) -> dict:
    """Analyze sentiment of news articles using OpenAI"""
    from fin_ai.clients.openai_client import chat_completion
    
    if not articles:
        return {
            "sentiment": "neutral",
            "confidence": 0.0,
            "summary": "No recent news found for this stock.",
            "key_points": []
        }
    
    # Prepare article summaries
    article_summaries = []
    for i, article in enumerate(articles[:5]):  # Use top 5 articles
        summary = f"{i+1}. {article.get('title', 'N/A')}\n   Source: {article.get('source', {}).get('name', 'Unknown')}"
        article_summaries.append(summary)
    
    articles_text = "\n".join(article_summaries)
    
    prompt = f"""Analyze the sentiment of these recent news articles about {symbol} stock and provide:
1. Overall sentiment (positive, negative, or neutral)
2. Confidence level (0-100)
3. Brief summary of market impact
4. Key points affecting stock price

News Articles:
{articles_text}

Respond in JSON format:
{{
    "sentiment": "positive|negative|neutral",
    "confidence": 0-100,
    "summary": "brief summary",
    "key_points": ["point1", "point2", "point3"]
}}"""
    
    try:
        response = chat_completion(prompt, model="gpt-3.5-turbo")
        
        # Try to parse JSON response
        import json
        import re
        
        # Extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            analysis = json.loads(json_match.group())
            return {
                "sentiment": analysis.get("sentiment", "neutral"),
                "confidence": analysis.get("confidence", 50),
                "summary": analysis.get("summary", ""),
                "key_points": analysis.get("key_points", [])
            }
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
    
    return {
        "sentiment": "neutral",
        "confidence": 50,
        "summary": f"Analyzed {len(articles)} articles but couldn't determine clear sentiment.",
        "key_points": []
    }


def generate_ai_prediction(
    symbol: str,
    news_sentiment: str,
    price_trend: str,
    news_summary: str,
    confidence_from_news: float
) -> tuple[str, float, str]:
    """Generate intelligent AI prediction based on news and price data"""
    
    # Combine signals
    sentiment_score = {"positive": 100, "neutral": 50, "negative": 0}.get(news_sentiment, 50)
    trend_score = {"up": 100, "neutral": 50, "down": 0}.get(price_trend, 50)
    
    # Weighted average (60% news, 40% price trend)
    combined_score = (sentiment_score * 0.6) + (trend_score * 0.4)
    
    # Determine prediction
    if combined_score >= 65:
        prediction = "up"
        confidence = min(confidence_from_news * 0.01 + 0.5, 0.95)
    elif combined_score <= 35:
        prediction = "down"
        confidence = min((100 - confidence_from_news) * 0.01 + 0.5, 0.95)
    else:
        prediction = "neutral"
        confidence = 0.5
    
    # Generate reasoning
    reasoning = f"Prediction based on: {news_sentiment} sentiment ({confidence_from_news}% confidence) from latest news + {price_trend} price trend. {news_summary}"
    
    return prediction, confidence, reasoning


@router.post("/create", response_model=PredictionResponse)
async def create_prediction(
    prediction: PredictionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a stock price prediction, optionally analyzing latest news"""
    from fin_ai.core.validation import is_valid_ticker

    # Validate symbol
    if not is_valid_ticker(prediction.stock_symbol):
        raise HTTPException(status_code=400, detail="Invalid stock symbol. Use standard ticker like AAPL or MSFT.")

    # Default AI prediction
    ai_prediction = "neutral"
    confidence_score = prediction.confidence_score
    reasoning = prediction.reasoning or "No reasoning provided"
    news_sentiment = None
    related_news_ids = None
    price_trend = None
    prediction_factors = None
    news_impact_score = 0.0
    
    # If user wants news analysis, fetch and analyze it
    if prediction.use_news_analysis:
        try:
            # Fetch news and price data concurrently
            news_articles, price_data = await asyncio.gather(
                fetch_news_for_stock(prediction.stock_symbol),
                fetch_price_data(prediction.stock_symbol)
            )
            
            price_trend = price_data.get("trend", "neutral")
            
            if news_articles:
                # Analyze sentiment
                sentiment_analysis = analyze_news_sentiment(news_articles, prediction.stock_symbol)
                news_sentiment = sentiment_analysis["sentiment"]
                news_impact_score = sentiment_analysis["confidence"]
                
                # Generate AI prediction
                ai_prediction, confidence_score, reasoning = generate_ai_prediction(
                    prediction.stock_symbol,
                    news_sentiment,
                    price_trend,
                    sentiment_analysis["summary"],
                    news_impact_score
                )
                
                # Store which news articles were used
                news_ids = [article.get("url", "")[:50] for article in news_articles[:5]]
                related_news_ids = ",".join(news_ids)
                
                # Create detailed prediction factors
                prediction_factors = f"""
News Sentiment: {news_sentiment} ({news_impact_score}% confidence)
Price Trend: {price_trend}
Recent Articles:
- {sentiment_analysis['summary']}

Key Factors:
{chr(10).join(f'• {point}' for point in sentiment_analysis.get('key_points', []))}
                """.strip()
        except Exception as e:
            print(f"Error in news analysis: {e}")
            # Fallback to simple prediction
            ai_prediction = "neutral"
            confidence_score = prediction.confidence_score
    
    # Create prediction in database
    new_prediction = Prediction(
        user_id=current_user.id,
        stock_symbol=prediction.stock_symbol.upper(),
        user_prediction=prediction.user_prediction,
        ai_prediction=ai_prediction,
        confidence_score=confidence_score,
        reasoning=reasoning,
        news_sentiment=news_sentiment,
        related_news_ids=related_news_ids,
        price_trend=price_trend,
        prediction_factors=prediction_factors,
        news_impact_score=news_impact_score
    )
    
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    return new_prediction


# Additional helper endpoints used by frontend before DB functionality
@router.get("/analyze")
async def analyze_prediction(symbol: str = "AAPL"):
    """Analyze and predict for a given stock symbol"""
    # Return mock prediction data if backend APIs are unavailable
    return {
        "aiForecast": {
            "direction": "up",
            "confidence": 0.75,
            "predictedPrice": 185
        },
        "indicators": [
            {"name": "RSI", "value": 58, "status": "neutral"},
            {"name": "MACD", "value": "bullish crossover", "status": "positive"},
            {"name": "Moving Average", "value": "above 200 EMA", "status": "positive"}
        ],
        "marketReality": {
            "actualPrice": 178,
            "volume": 32000000,
            "change": 2.3
        },
        "comparison": {
            "userPrediction": "up",
            "aiPrediction": "up",
            "accuracy": "Correct"
        },
        "scorecard": {
            "totalPredictions": 10,
            "correctPredictions": 7,
            "winRate": "70%"
        }
    }


@router.post("/submit")
async def submit_prediction(data: dict):
    """Submit a user prediction"""
    return {
        "success": True,
        "predictionId": "pred_" + datetime.utcnow().timestamp().__str__(),
        "message": "Prediction submitted successfully",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/my-predictions", response_model=list[PredictionResponse])
def get_user_predictions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's predictions"""
    predictions = db.query(Prediction).filter(Prediction.user_id == current_user.id).order_by(Prediction.prediction_date.desc()).all()
    return predictions


@router.get("/{prediction_id}", response_model=PredictionResponse)
def get_prediction(prediction_id: str, db: Session = Depends(get_db)):
    """Get prediction by ID"""
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction


@router.post("/{prediction_id}/evaluate", response_model=PredictionResponse)
def evaluate_prediction(
    prediction_id: str,
    eval_data: PredictionEvaluate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Evaluate prediction with actual outcome"""
    prediction = db.query(Prediction).filter(Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    if prediction.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    prediction.actual_outcome = eval_data.actual_outcome
    prediction.evaluation_date = datetime.utcnow()
    prediction.user_correct = prediction.user_prediction == eval_data.actual_outcome
    prediction.ai_correct = prediction.ai_prediction == eval_data.actual_outcome
    
    # Generate intelligent explanation
    explanation = generate_explanation(
        prediction.user_prediction,
        prediction.ai_prediction,
        eval_data.actual_outcome,
        prediction.reasoning,
        prediction.news_sentiment,
        prediction.prediction_factors
    )
    prediction.explanation = explanation
    
    db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


@router.get("/stats/overview")
def get_prediction_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get prediction statistics"""
    predictions = db.query(Prediction).filter(Prediction.user_id == current_user.id).all()
    
    total = len(predictions)
    evaluated = len([p for p in predictions if p.actual_outcome])
    user_correct = len([p for p in predictions if p.user_correct == True])
    ai_correct = len([p for p in predictions if p.ai_correct == True])
    news_based = len([p for p in predictions if p.news_sentiment])
    news_based_correct = len([p for p in predictions if p.news_sentiment and p.ai_correct == True])
    
    user_accuracy = (user_correct / evaluated * 100) if evaluated > 0 else 0
    ai_accuracy = (ai_correct / evaluated * 100) if evaluated > 0 else 0
    news_accuracy = (news_based_correct / news_based * 100) if news_based > 0 else 0
    
    return {
        "total_predictions": total,
        "evaluated_predictions": evaluated,
        "user_correct": user_correct,
        "ai_correct": ai_correct,
        "user_accuracy": user_accuracy,
        "ai_accuracy": ai_accuracy,
        "news_based_predictions": news_based,
        "news_based_accuracy": news_accuracy
    }


def generate_explanation(
    user_prediction: str,
    ai_prediction: str,
    actual: str,
    reasoning: str,
    news_sentiment: Optional[str] = None,
    prediction_factors: Optional[str] = None
) -> str:
    """Generate intelligent explanation for prediction outcome"""
    
    news_context = ""
    if news_sentiment:
        news_context = f"\n📰 **News Impact**: The {news_sentiment} sentiment from recent news influenced the prediction."
    
    factors_context = ""
    if prediction_factors:
        factors_context = f"\n**Analysis Factors**:\n{prediction_factors}"
    
    if user_prediction == actual and ai_prediction == actual:
        return f"✅ **Both Correct!** You and the AI predicted {actual}. Excellent timing!\n\n{reasoning}{news_context}{factors_context}"
    elif user_prediction == actual:
        return f"🎯 **You Won!** Your prediction of {actual} was correct, while the AI predicted {ai_prediction}. Your market insight was better!\n\n{reasoning}{news_context}{factors_context}"
    elif ai_prediction == actual:
        return f"📊 **AI Won!** The AI's prediction of {actual} was correct, while you predicted {user_prediction}. The news analysis and market data were key factors.\n\n{reasoning}{news_context}{factors_context}"
    else:
        return f"❌ **Both Incorrect.** Market moved {actual}, surprising both predictions ({user_prediction} vs AI's {ai_prediction}). Markets can be unpredictable.\n\n{reasoning}{news_context}{factors_context}"


# New endpoints for frontend compatibility
@router.get("/analyze")
async def analyze_prediction(symbol: str = "AAPL"):
    """Analyze and predict for a given stock symbol"""
    # Return mock prediction data if backend APIs are unavailable
    return {
        "aiForecast": {
            "direction": "up",
            "confidence": 0.75,
            "predictedPrice": 185
        },
        "indicators": [
            {"name": "RSI", "value": 58, "status": "neutral"},
            {"name": "MACD", "value": "bullish crossover", "status": "positive"},
            {"name": "Moving Average", "value": "above 200 EMA", "status": "positive"}
        ],
        "marketReality": {
            "actualPrice": 178,
            "volume": 32000000,
            "change": 2.3
        },
        "comparison": {
            "userPrediction": "up",
            "aiPrediction": "up",
            "accuracy": "Correct"
        },
        "scorecard": {
            "totalPredictions": 10,
            "correctPredictions": 7,
            "winRate": "70%"
        }
    }


@router.post("/submit")
async def submit_prediction(data: dict):
    """Submit a user prediction"""
    return {
        "success": True,
        "predictionId": "pred_" + datetime.utcnow().timestamp().__str__(),
        "message": "Prediction submitted successfully",
        "timestamp": datetime.utcnow().isoformat()
    }
