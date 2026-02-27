from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

# ==================== Auth Schemas ====================
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


# ==================== Learning Schemas ====================
class LearningModuleResponse(BaseModel):
    id: str
    title: str
    description: str
    content: str
    difficulty_level: str
    order: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserLearningProgressResponse(BaseModel):
    id: str
    user_id: str
    module_id: str
    completed: bool
    progress_percentage: float
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AssessmentResponse(BaseModel):
    id: str
    title: str
    description: str
    module_id: str

    class Config:
        from_attributes = True


class UserAssessmentSubmit(BaseModel):
    assessment_id: str
    answers: dict


class UserAssessmentResponse(BaseModel):
    id: str
    user_id: str
    assessment_id: str
    score: Optional[float] = None
    completed: bool
    submitted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ==================== Quiz Schemas ====================
class QuizCreate(BaseModel):
    module_id: str
    title: str
    difficulty: str = "beginner"
    question_count: int = 5


class QuizQuestionResponse(BaseModel):
    id: str
    prompt: str
    choices: Optional[str] = None
    order: int

    class Config:
        from_attributes = True


class QuizResponse(BaseModel):
    id: str
    module_id: str
    title: str
    difficulty: str
    question_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class QuizInstanceCreate(BaseModel):
    quiz_id: str


class QuizAnswerSubmit(BaseModel):
    question_id: str
    answer: str


class QuizSubmitRequest(BaseModel):
    answers: List[QuizAnswerSubmit]


class QuizResultResponse(BaseModel):
    instance_id: str
    quiz_id: str
    user_id: str
    score: float
    completed: bool
    submitted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProgressSummary(BaseModel):
    total_modules: int
    completed_modules: int
    average_score: float


class ProgressTrendPoint(BaseModel):
    date: datetime
    score: float


class ProgressTrends(BaseModel):
    module_id: str
    trends: List[ProgressTrendPoint]


# ==================== Paper Trading Schemas ====================
class PaperTradeCreate(BaseModel):
    stock_symbol: str
    action: str  # buy or sell
    quantity: float
    target_days: int = 1  # evaluate after N days
    create_prediction: bool = True


class PaperTradeResponse(BaseModel):
    id: str
    user_id: str
    stock_symbol: str
    action: str
    quantity: float
    entry_price: Optional[float] = None
    entry_date: datetime
    target_date: Optional[datetime] = None
    settled: bool
    exit_price: Optional[float] = None
    pnl: Optional[float] = None
    linked_prediction_id: Optional[str] = None
    explanation: Optional[str] = None

    class Config:
        from_attributes = True


# ==================== Stock Prediction Schemas ====================
class PredictionCreate(BaseModel):
    stock_symbol: str
    user_prediction: str  # up, down, neutral
    confidence_score: float = 0.5
    reasoning: Optional[str] = None
    use_news_analysis: bool = True  # Analyze latest news for this prediction


class PredictionResponse(BaseModel):
    id: str
    user_id: str
    stock_symbol: str
    user_prediction: str
    ai_prediction: str
    actual_outcome: Optional[str] = None
    confidence_score: float
    reasoning: Optional[str] = None
    prediction_date: datetime
    user_correct: Optional[bool] = None
    ai_correct: Optional[bool] = None
    explanation: Optional[str] = None
    # News-based prediction fields
    related_news_ids: Optional[str] = None
    news_sentiment: Optional[str] = None
    price_trend: Optional[str] = None
    prediction_factors: Optional[str] = None
    news_impact_score: float = 0.0

    class Config:
        from_attributes = True


class PredictionEvaluate(BaseModel):
    actual_outcome: str  # up, down, neutral


# ==================== News Schemas ====================
class FinancialNewsResponse(BaseModel):
    id: str
    title: str
    content: str
    source: str
    related_symbols: Optional[str] = None
    sentiment: Optional[str] = None
    market_impact: Optional[str] = None
    impact_explanation: Optional[str] = None
    published_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Portfolio Schemas ====================
class PortfolioHoldingResponse(BaseModel):
    id: str
    stock_symbol: str
    quantity: float
    purchase_price: float
    current_price: float
    total_cost: float
    current_value: float
    gain_loss: float
    gain_loss_percentage: float
    purchased_at: datetime

    class Config:
        from_attributes = True


class PortfolioResponse(BaseModel):
    id: str
    user_id: str
    total_value: float
    cash_balance: float
    total_return: float
    total_return_percentage: float
    holdings: List[PortfolioHoldingResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class BuyStock(BaseModel):
    stock_symbol: str
    quantity: float
    price: float


class SellStock(BaseModel):
    stock_symbol: str
    quantity: float
    price: float


# ==================== Chat Schemas ====================
class ConversationMessageCreate(BaseModel):
    content: str


class ConversationMessageResponse(BaseModel):
    id: str
    role: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: str
    title: Optional[str] = None
    created_at: datetime
    messages: List[ConversationMessageResponse] = []

    class Config:
        from_attributes = True