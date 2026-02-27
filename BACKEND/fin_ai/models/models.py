from sqlalchemy import Column, String, DateTime, Integer, Float, Boolean, Text, Enum
import uuid
from datetime import datetime
import enum

# use the shared Base from database so metadata.create_all works correctly
from ..database import Base

# ==================== User & Auth ====================
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ==================== Finance Learning ====================
class LearningModule(Base):
    __tablename__ = "learning_modules"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    difficulty_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserLearningProgress(Base):
    __tablename__ = "user_learning_progress"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    module_id = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    progress_percentage = Column(Float, default=0.0)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    module_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class UserAssessment(Base):
    __tablename__ = "user_assessments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    assessment_id = Column(String, nullable=False)
    score = Column(Float, nullable=True)
    completed = Column(Boolean, default=False)
    submitted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# ==================== Learning: Quizzes ====================
class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    module_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    difficulty = Column(String, default="beginner")
    question_count = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)


class QuizQuestion(Base):
    __tablename__ = "quiz_questions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    quiz_id = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    choices = Column(Text, nullable=True)  # JSON or comma-separated
    correct_answer = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class QuizInstance(Base):
    __tablename__ = "quiz_instances"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    quiz_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    score = Column(Float, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class QuizAnswer(Base):
    __tablename__ = "quiz_answers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    instance_id = Column(String, nullable=False)
    question_id = Column(String, nullable=False)
    answer = Column(Text, nullable=True)
    correct = Column(Boolean, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)



# ==================== Stock Prediction ====================
class PredictionClass(str, enum.Enum):
    UP = "up"
    DOWN = "down"
    NEUTRAL = "neutral"


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    stock_symbol = Column(String, nullable=False)
    user_prediction = Column(String, nullable=False)  # up, down, neutral
    ai_prediction = Column(String, nullable=False)  # up, down, neutral
    actual_outcome = Column(String, nullable=True)  # up, down, neutral
    confidence_score = Column(Float, default=0.0)
    reasoning = Column(Text, nullable=True)
    prediction_date = Column(DateTime, default=datetime.utcnow)
    evaluation_date = Column(DateTime, nullable=True)
    user_correct = Column(Boolean, nullable=True)
    ai_correct = Column(Boolean, nullable=True)
    explanation = Column(Text, nullable=True)  # Intelligent explanation of outcome
    # News-based prediction fields
    related_news_ids = Column(String, nullable=True)  # comma-separated news IDs
    news_sentiment = Column(String, nullable=True)  # positive, negative, neutral
    price_trend = Column(String, nullable=True)  # up, down, stable
    prediction_factors = Column(Text, nullable=True)  # detailed factors considered
    news_impact_score = Column(Float, default=0.0)  # 0-100, how much news influenced prediction


# ==================== Financial News ====================
class FinancialNews(Base):
    __tablename__ = "financial_news"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String, nullable=False)
    related_symbols = Column(String, nullable=True)  # comma-separated stock symbols
    sentiment = Column(String, nullable=True)  # positive, negative, neutral
    market_impact = Column(String, nullable=True)  # high, medium, low
    impact_explanation = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# ==================== Portfolio ====================
class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, unique=True)
    total_value = Column(Float, default=0.0)
    cash_balance = Column(Float, default=10000.0)
    total_return = Column(Float, default=0.0)
    total_return_percentage = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PortfolioHolding(Base):
    __tablename__ = "portfolio_holdings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    portfolio_id = Column(String, nullable=False)
    stock_symbol = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    purchase_price = Column(Float, nullable=False)
    current_price = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    current_value = Column(Float, nullable=False)
    gain_loss = Column(Float, default=0.0)
    gain_loss_percentage = Column(Float, default=0.0)
    purchased_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ==================== AI Strategy Advisor ====================
class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ConversationMessage(Base):
    __tablename__ = "conversation_messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    role = Column(String, nullable=False)  # user or assistant
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


# ==================== Paper Trading ====================
class PaperTrade(Base):
    __tablename__ = "paper_trades"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    stock_symbol = Column(String, nullable=False)
    action = Column(String, nullable=False)  # buy or sell
    quantity = Column(Float, nullable=False, default=0.0)
    entry_price = Column(Float, nullable=True)
    entry_date = Column(DateTime, default=datetime.utcnow)
    target_date = Column(DateTime, nullable=True)  # date to evaluate outcome
    settled = Column(Boolean, default=False)
    exit_price = Column(Float, nullable=True)
    pnl = Column(Float, nullable=True)
    linked_prediction_id = Column(String, nullable=True)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)