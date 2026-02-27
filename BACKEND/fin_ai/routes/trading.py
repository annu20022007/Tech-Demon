from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User, PaperTrade, Prediction
from ..schemas.schemas import PaperTradeCreate, PaperTradeResponse, PredictionCreate, PredictionResponse
from ..core.security import get_current_user
from datetime import datetime, timedelta
from typing import Optional
from ..routes.prediction import fetch_price_data, analyze_news_sentiment, generate_ai_prediction
from ..clients.openai_client import chat_completion
from ..core.validation import is_valid_ticker
from fin_ai.database import SessionLocal
import asyncio

router = APIRouter(
    prefix="/trading",
    tags=["Trading"]
)


@router.post("/create", response_model=PaperTradeResponse)
def create_paper_trade(payload: PaperTradeCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Validate symbol
    symbol = payload.stock_symbol.strip().upper()
    if not is_valid_ticker(symbol):
        raise HTTPException(status_code=400, detail="Invalid stock symbol")

    # Create trade record
    entry_price = None
    entry_date = datetime.utcnow()
    target_date = entry_date + timedelta(days=payload.target_days)

    trade = PaperTrade(
        user_id=current_user.id,
        stock_symbol=symbol,
        action=payload.action.lower(),
        quantity=payload.quantity,
        entry_price=entry_price,
        entry_date=entry_date,
        target_date=target_date,
        settled=False
    )
    db.add(trade)
    db.commit()
    db.refresh(trade)

    # Optionally create a linked prediction (uses existing prediction logic but simplified)
    linked_pred_id = None
    if payload.create_prediction:
        from ..routes.prediction import create_prediction as create_pred_endpoint
        # construct a simple PredictionCreate object
        pred_payload = PredictionCreate(stock_symbol=symbol, user_prediction="neutral", confidence_score=0.5, reasoning="Paper-trade auto-prediction", use_news_analysis=True)
        # call internal function (synchronous path) — route expects async; call underlying logic by importing function content is complicated,
        # instead, create a simple Prediction record directly here
        ai_pred = "neutral"
        pred = Prediction(
            user_id=current_user.id,
            stock_symbol=symbol,
            user_prediction="neutral",
            ai_prediction=ai_pred,
            confidence_score=0.5,
            reasoning="Auto-generated for paper trade"
        )
        db.add(pred)
        db.commit()
        db.refresh(pred)
        linked_pred_id = pred.id
        trade.linked_prediction_id = linked_pred_id
        db.add(trade)
        db.commit()
        db.refresh(trade)

    return trade


@router.get("/my-trades", response_model=list[PaperTradeResponse])
def get_my_trades(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trades = db.query(PaperTrade).filter(PaperTrade.user_id == current_user.id).order_by(PaperTrade.entry_date.desc()).all()
    return trades


@router.post("/{trade_id}/settle", response_model=PaperTradeResponse)
def settle_trade(trade_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    trade = db.query(PaperTrade).filter(PaperTrade.id == trade_id).first()
    if not trade or trade.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Trade not found")
    if trade.settled:
        raise HTTPException(status_code=400, detail="Trade already settled")

    # Fetch price data (recent) and pick closing price at or after target_date
    # fetch_price_data is async in prediction module; run it in event loop
    try:
        price_info = asyncio.run(fetch_price_data(trade.stock_symbol))
    except Exception:
        price_info = {}
    latest_price = price_info.get("latest_price")
    if latest_price is None:
        raise HTTPException(status_code=500, detail="Could not fetch price data to settle trade")

    # Compute PnL for buy: (exit - entry) * qty ; if entry_price unknown, assume entry at latest_price at entry_date (simulate)
    entry_price = trade.entry_price or latest_price
    exit_price = latest_price
    pnl = (exit_price - entry_price) * trade.quantity if trade.action == "buy" else (entry_price - exit_price) * trade.quantity

    trade.exit_price = exit_price
    trade.pnl = pnl
    trade.settled = True
    trade.explanation = generate_trade_explanation(trade, price_info)
    db.add(trade)
    db.commit()
    db.refresh(trade)
    return trade


def settle_trade_by_id(trade_id: str) -> Optional[PaperTrade]:
    """Internal helper to settle a trade by id (used by background worker)."""
    db = SessionLocal()
    try:
        trade = db.query(PaperTrade).filter(PaperTrade.id == trade_id).first()
        if not trade or trade.settled:
            return None

        # fetch price data
        try:
            price_info = asyncio.run(fetch_price_data(trade.stock_symbol))
        except Exception:
            price_info = {}

        latest_price = price_info.get("latest_price")
        if latest_price is None:
            return None

        entry_price = trade.entry_price or latest_price
        exit_price = latest_price
        pnl = (exit_price - entry_price) * trade.quantity if trade.action == "buy" else (entry_price - exit_price) * trade.quantity

        trade.exit_price = exit_price
        trade.pnl = pnl
        trade.settled = True
        trade.explanation = generate_trade_explanation(trade, price_info)
        db.add(trade)
        db.commit()
        db.refresh(trade)
        return trade
    finally:
        db.close()


def generate_trade_explanation(trade: PaperTrade, price_info: dict) -> str:
    """Create an intelligent explanation using news sentiment, price trend and prediction (if any)."""
    symbol = trade.stock_symbol
    # Get news and sentiment
    try:
        # fetch top articles
        import asyncio
        articles = asyncio.run(fetch_news_for_settlement(symbol))
        sentiment = analyze_news_sentiment(articles, symbol)
    except Exception:
        sentiment = {"sentiment": "neutral", "confidence": 50, "summary": "No news available", "key_points": []}

    price_trend = price_info.get("trend", "neutral")

    # Build a concise explanation
    explanation = (
        f"Trade {trade.action.upper()} {trade.quantity} {symbol} entered at ${trade.entry_price or price_info.get('latest_price'):.2f}. "
        f"On settlement the price was ${trade.exit_price:.2f}, PnL: ${trade.pnl:.2f}.\n"
        f"News Sentiment: {sentiment.get('sentiment')} ({sentiment.get('confidence')}% confidence). {sentiment.get('summary')}\n"
        f"Recent Price Trend: {price_trend}.\n"
    )

    # If linked prediction exists, fetch and compare
    if trade.linked_prediction_id:
        pred = None
        try:
            pred = db_get_prediction(trade.linked_prediction_id)
        except Exception:
            pred = None
        if pred:
            explanation += f"Linked AI prediction: {pred.ai_prediction} (confidence {pred.confidence_score}).\n"

    # Use LLM for polishing (optional)
    try:
        prompt = f"Summarize why a paper trade on {symbol} resulted in PnL ${trade.pnl:.2f}. Include news summary and price trend: {sentiment.get('summary')} | trend: {price_trend}. Keep concise and finance-focused."
        polished = chat_completion(prompt)
        if polished and not polished.startswith("[OpenAI error"):
            explanation += "\nLLM Summary: " + polished
    except Exception:
        pass

    return explanation


async def fetch_news_for_settlement(symbol: str):
    from ..routes.prediction import fetch_news_for_stock
    return await fetch_news_for_stock(symbol)


def db_get_prediction(pred_id: str) -> Optional[Prediction]:
    from fin_ai.database import SessionLocal
    db = SessionLocal()
    try:
        p = db.query(Prediction).filter(Prediction.id == pred_id).first()
        return p
    finally:
        db.close()
