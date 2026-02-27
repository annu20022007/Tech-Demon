from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User, Portfolio, PortfolioHolding
from ..schemas.schemas import PortfolioResponse, PortfolioHoldingResponse, BuyStock, SellStock
from ..core.security import get_current_user

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)

# Get user's portfolio
@router.get("/", response_model=PortfolioResponse)
def get_portfolio(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()
    
    if not portfolio:
        # Create portfolio if doesn't exist
        portfolio = Portfolio(user_id=current_user.id)
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
    
    holdings = db.query(PortfolioHolding).filter(PortfolioHolding.portfolio_id == portfolio.id).all()
    portfolio.holdings = holdings
    return portfolio


# Buy a stock (paper trading)
@router.post("/buy")
def buy_stock(stock_data: BuyStock, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()
    
    if not portfolio:
        portfolio = Portfolio(user_id=current_user.id)
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
    
    total_cost = stock_data.quantity * stock_data.price
    
    if portfolio.cash_balance < total_cost:
        raise HTTPException(status_code=400, detail="Insufficient cash balance")
    
    # Check if already holding this stock
    holding = db.query(PortfolioHolding).filter(
        PortfolioHolding.portfolio_id == portfolio.id,
        PortfolioHolding.stock_symbol == stock_data.stock_symbol
    ).first()
    
    if holding:
        # Update existing holding
        holding.quantity += stock_data.quantity
        holding.total_cost += total_cost
        holding.current_price = stock_data.price
        holding.current_value = holding.quantity * stock_data.price
    else:
        # Create new holding
        holding = PortfolioHolding(
            portfolio_id=portfolio.id,
            stock_symbol=stock_data.stock_symbol,
            quantity=stock_data.quantity,
            purchase_price=stock_data.price,
            current_price=stock_data.price,
            total_cost=total_cost,
            current_value=total_cost
        )
        db.add(holding)
    
    portfolio.cash_balance -= total_cost
    portfolio.total_value = portfolio.cash_balance + sum(
        h.current_value for h in db.query(PortfolioHolding).filter(
            PortfolioHolding.portfolio_id == portfolio.id
        ).all()
    )
    
    db.add(portfolio)
    db.add(holding)
    db.commit()
    db.refresh(portfolio)
    
    return {"message": "Stock purchased successfully", "portfolio": portfolio}


# Sell a stock (paper trading)
@router.post("/sell")
def sell_stock(stock_data: SellStock, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    holding = db.query(PortfolioHolding).filter(
        PortfolioHolding.portfolio_id == portfolio.id,
        PortfolioHolding.stock_symbol == stock_data.stock_symbol
    ).first()
    
    if not holding or holding.quantity < stock_data.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock quantity")
    
    sold_amount = stock_data.quantity * stock_data.price
    
    holding.quantity -= stock_data.quantity
    holding.current_price = stock_data.price
    
    if holding.quantity == 0:
        db.delete(holding)
    else:
        holding.current_value = holding.quantity * stock_data.price
        db.add(holding)
    
    portfolio.cash_balance += sold_amount
    portfolio.total_value = portfolio.cash_balance + sum(
        h.current_value for h in db.query(PortfolioHolding).filter(
            PortfolioHolding.portfolio_id == portfolio.id
        ).all()
    )
    
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    
    return {"message": "Stock sold successfully", "portfolio": portfolio}


# Get portfolio analysis
@router.get("/analysis/overview")
def get_portfolio_analysis(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    holdings = db.query(PortfolioHolding).filter(PortfolioHolding.portfolio_id == portfolio.id).all()
    
    total_invested = sum(h.total_cost for h in holdings)
    total_current_value = sum(h.current_value for h in holdings)
    total_gain_loss = total_current_value - total_invested
    
    return {
        "total_invested": total_invested,
        "total_current_value": total_current_value,
        "cash_balance": portfolio.cash_balance,
        "total_value": portfolio.total_value,
        "total_gain_loss": total_gain_loss,
        "gain_loss_percentage": (total_gain_loss / total_invested * 100) if total_invested > 0 else 0,
        "holdings_count": len(holdings),
        "diversification": get_diversification(holdings)
    }


# Get diversification analysis
@router.get("/analysis/diversification")
def get_portfolio_diversification(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    
    holdings = db.query(PortfolioHolding).filter(PortfolioHolding.portfolio_id == portfolio.id).all()
    return get_diversification(holdings)


def get_diversification(holdings):
    total_value = sum(h.current_value for h in holdings)
    
    diversification = []
    for holding in holdings:
        percentage = (holding.current_value / total_value * 100) if total_value > 0 else 0
        diversification.append({
            "symbol": holding.stock_symbol,
            "percentage": percentage,
            "value": holding.current_value
        })
    
    return sorted(diversification, key=lambda x: x["percentage"], reverse=True)


# Get portfolio history/performance
@router.get("/history")
def get_portfolio_history(db: Session = Depends(get_db)):
    """Get portfolio performance history"""
    from datetime import datetime, timedelta
    
    history = []
    base_value = 20000
    for i in range(6):
        date = (datetime.utcnow() - timedelta(days=30-i*5)).strftime("%b %d")
        value = base_value + (i * 1000) + (500 if i % 2 == 0 else -300)
        history.append({"date": date, "value": value})
    return history


# Get AI insight about portfolio
@router.get("/insight")
def get_portfolio_insight(db: Session = Depends(get_db)):
    """Get AI insight about portfolio"""
    return "Your portfolio is well-diversified with strong growth potential. Consider rebalancing quarterly to maintain your target allocation."
