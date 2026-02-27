from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User, Conversation, ConversationMessage
from ..schemas.schemas import ConversationResponse, ConversationMessageCreate, ConversationMessageResponse
from ..core.security import get_current_user
from typing import List

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

# Create a new conversation
@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = Conversation(user_id=current_user.id)
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


# Get user's conversations
@router.get("/conversations", response_model=List[ConversationResponse])
def get_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversations = db.query(Conversation).filter(Conversation.user_id == current_user.id).all()
    
    for conv in conversations:
        messages = db.query(ConversationMessage).filter(
            ConversationMessage.conversation_id == conv.id
        ).all()
        conv.messages = messages
    
    return conversations


# Get specific conversation
@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(conversation_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation or conversation.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(ConversationMessage).filter(
        ConversationMessage.conversation_id == conversation_id
    ).all()
    conversation.messages = messages
    return conversation


# Send message to AI advisor
@router.post("/conversations/{conversation_id}/messages", response_model=ConversationMessageResponse)
def send_message(
    conversation_id: str,
    message_data: ConversationMessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation or conversation.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Save user message
    user_message = ConversationMessage(
        conversation_id=conversation_id,
        user_id=current_user.id,
        role="user",
        content=message_data.content
    )
    db.add(user_message)
    db.commit()
    
    # Generate AI response
    try:
        ai_response = generate_ai_response(
            message_data.content,
            current_user.id,
            db
        )
    except Exception:
        # fallback to OpenAI chat client
        from fin_ai.clients.openai_client import chat_completion
        ai_response = chat_completion(message_data.content)
    
    # Save AI message
    ai_message = ConversationMessage(
        conversation_id=conversation_id,
        user_id=current_user.id,
        role="assistant",
        content=ai_response
    )
    db.add(ai_message)
    db.commit()
    db.refresh(ai_message)
    
    return ai_message


# Get all messages in conversation
@router.get("/conversations/{conversation_id}/messages", response_model=List[ConversationMessageResponse])
def get_messages(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation or conversation.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    messages = db.query(ConversationMessage).filter(
        ConversationMessage.conversation_id == conversation_id
    ).all()
    return messages


def generate_ai_response(user_query: str, user_id: str, db: Session) -> str:
    """
    Generate AI response based on user query and portfolio insights.
    Enforce finance-only responses using heuristic validation.
    """
    from fin_ai.core.validation import is_finance_query

    # If query is clearly non-financial, refuse politely
    try:
        if not is_finance_query(user_query):
            return "I'm here to help with finance-related questions only. Please ask about markets, stocks, portfolios, or related financial topics."
    except Exception:
        pass

    query_lower = user_query.lower()
    
    # Query detection and response generation
    if any(keyword in query_lower for keyword in ["portfolio", "holding", "stock"]):
        return generate_portfolio_advice(user_id, db, user_query)
    elif any(keyword in query_lower for keyword in ["market", "news", "trend"]):
        return generate_market_advice(db, user_query)
    elif any(keyword in query_lower for keyword in ["predict", "forecast", "bull", "bear"]):
        return generate_prediction_advice(user_query)
    elif any(keyword in query_lower for keyword in ["learn", "strategy", "risk"]):
        return generate_strategy_advice(user_query)
    else:
        return generate_general_finance_advice(user_query)


def generate_portfolio_advice(user_id: str, db: Session, query: str) -> str:
    """Generate advice about user's portfolio"""
    from fin_ai.models.models import Portfolio
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == user_id).first()
    
    if not portfolio:
        return "I don't have portfolio data for you yet. Start by adding stocks to your portfolio to get personalized advice!"
    
    return (
        f"Based on your portfolio:\n"
        f"- Total Value: ${portfolio.total_value:.2f}\n"
        f"- Cash Balance: ${portfolio.cash_balance:.2f}\n"
        f"- Total Return: {portfolio.total_return_percentage:.2f}%\n\n"
        f"Regarding your query about '{query}':\n"
        f"To improve your portfolio performance, consider:\n"
        f"1. Diversifying across different sectors\n"
        f"2. Regular rebalancing (monthly or quarterly)\n"
        f"3. Not trying to time the market\n"
        f"4. Maintaining an emergency cash reserve\n"
        f"5. Following a long-term investment strategy"
    )


def generate_market_advice(db: Session, query: str) -> str:
    """Generate advice about market trends"""
    return (
        f"Regarding the market and news perspective on '{query}':\n\n"
        f"Key considerations:\n"
        f"1. **Market Sentiment**: Monitor the overall sentiment from financial news.\n"
        f"2. **Economic Indicators**: Watch Fed decisions, inflation rates, and employment data.\n"
        f"3. **Sector Rotation**: Different sectors perform better in different market conditions.\n"
        f"4. **Risk Management**: Use stop-loss orders to protect your investments.\n"
        f"5. **News Impact**: Be cautious of panic selling due to temporary news shocks.\n\n"
        f"Would you like to review the latest news analysis or check trending stocks?"
    )


def generate_prediction_advice(query: str) -> str:
    """Generate advice about predicting market movements"""
    return (
        f"Regarding stock price predictions ('{query}'):\n\n"
        f"Important observations:\n"
        f"1. **Historical patterns don't guarantee future results**: Past performance isn't indicative of future results.\n"
        f"2. **Technical Analysis**: Learn candlestick patterns, support/resistance levels, moving averages.\n"
        f"3. **Fundamental Analysis**: Understand P/E ratios, earnings, and business fundamentals.\n"
        f"4. **Market Psychology**: Understand fear and greed cycles in markets.\n"
        f"5. **Probability Over Certainty**: Trading is about odds, not certainties.\n\n"
        f"Use our prediction playground to practice and compare with AI predictions!"
    )


def generate_strategy_advice(query: str) -> str:
    """Generate investment strategy advice"""
    return (
        f"For your query about '{query}':\n\n"
        f"**Strategic Approaches**:\n"
        f"1. **Value Investing**: Buy undervalued stocks with strong fundamentals (Buffett style).\n"
        f"2. **Growth Investing**: Focus on companies with high growth potential.\n"
        f"3. **Dividend Strategy**: Build passive income through dividend-paying stocks.\n"
        f"4. **Dollar-Cost Averaging**: Invest fixed amounts regularly to reduce timing risk.\n"
        f"5. **Index Investing**: Passive investing in market indices for steady returns.\n\n"
        f"**Risk Management**:\n"
        f"- Never invest money you can't afford to lose\n"
        f"- Diversify across sectors and asset classes\n"
        f"- Maintain adequate emergency funds\n"
        f"- Consider your time horizon and risk tolerance"
    )


def generate_general_finance_advice(query: str) -> str:
    """Generate general financial advice"""
    return (
        f"I'm your AI Financial Strategy Advisor, here to help with: '{query}'\n\n"
        f"I can assist you with:\n"
        f"✓ Portfolio analysis and optimization\n"
        f"✓ Stock prediction practice and analysis\n"
        f"✓ Market trend interpretation\n"
        f"✓ Investment strategy recommendations\n"
        f"✓ Risk management and diversification advice\n"
        f"✓ General finance education\n\n"
        f"What specific area would you like to explore? Try asking about:\n"
        f"- 'How should I allocate my portfolio?'\n"
        f"- 'What stocks are trending?'\n"
        f"- 'How to build a diversified portfolio?'\n"
        f"- 'What's the best investment strategy for beginners?'"
    )
