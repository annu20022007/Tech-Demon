# FinAI Backend - API Documentation

## 🚀 Backend Server Running!

Your FinAI backend is now running at: **http://localhost:8000**

### 📚 API Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔐 Features Implemented

### 1. **User Authentication & Profiles**
Secure login system with JWT tokens allowing users to manage their accounts.

#### Endpoints:
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get access token
- `GET /api/auth/me` - Get current user profile
- `PUT /api/auth/me` - Update user profile

**Example - Register:**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }
```

**Example - Login:**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d {
    "email": "john@example.com",
    "password": "securepassword123"
  }
```

---

### 2. **Finance Learning & Assessment Module**
Structured learning environment with modules and assessments.

#### Endpoints:
- `GET /api/learning/modules` - Get all learning modules
- `GET /api/learning/progress` - Get your learning progress
- `POST /api/learning/modules/{module_id}/complete` - Mark module complete
- `GET /api/learning/modules/{module_id}/assessments` - Get assessments for a module
- `POST /api/learning/assessments/{assessment_id}/submit` - Submit assessment
- `GET /api/learning/assessments` - Get your assessment results

**Example - Get Modules:**
```bash
curl -X GET "http://localhost:8000/api/learning/modules"
```

**Example - Submit Assessment:**
```bash
curl -X POST "http://localhost:8000/api/learning/assessments/assessment_id/submit" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d {
    "assessment_id": "assessment_id",
    "answers": {"q1": "answer1", "q2": "answer2"}
  }
```

---

### 3. **Stock Prediction Playground**
Interactive paper-trading arena for predictions with AI comparison.

#### Endpoints:
- `POST /api/predictions/create` - Make a stock prediction
- `GET /api/predictions/my-predictions` - Get all your predictions
- `GET /api/predictions/{prediction_id}` - Get prediction details
- `POST /api/predictions/{prediction_id}/evaluate` - Evaluate prediction with actual outcome
- `GET /api/predictions/stats/overview` - Get prediction statistics

**Example - Make Prediction:**
```bash
curl -X POST "http://localhost:8000/api/predictions/create" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d {
    "stock_symbol": "AAPL",
    "user_prediction": "up",
    "confidence_score": 0.75,
    "reasoning": "Strong earnings report expected"
  }
```

**Example - Evaluate Prediction:**
```bash
curl -X POST "http://localhost:8000/api/predictions/prediction_id/evaluate" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d {
    "actual_outcome": "up"
  }
```

---

### 4. **Financial News Intelligence Module**
Live news analysis with sentiment and market impact evaluation.

#### Endpoints:
- `GET /api/news/` - Get all financial news
- `GET /api/news/stock/{symbol}` - Get news for specific stock
- `GET /api/news/sentiment/{sentiment_type}` - Get news by sentiment
- `GET /api/news/impact/high` - Get high-impact news
- `GET /api/news/{news_id}` - Get news details
- `GET /api/news/summary/market-sentiment` - Get overall market sentiment
- `GET /api/news/trending/stocks` - Get trending stocks from news

**Example - Get Market Sentiment:**
```bash
curl -X GET "http://localhost:8000/api/news/summary/market-sentiment"
```

**Example - Get Trending Stocks:**
```bash
curl -X GET "http://localhost:8000/api/news/trending/stocks"
```

---

### 5. **Portfolio Analyzer**
Paper-trading portfolio with buy/sell functionality and analysis.

#### Endpoints:
- `GET /api/portfolio/` - Get your portfolio
- `POST /api/portfolio/buy` - Buy stocks (paper trading)
- `POST /api/portfolio/sell` - Sell stocks (paper trading)
- `GET /api/portfolio/analysis/overview` - Get portfolio analysis
- `GET /api/portfolio/analysis/diversification` - Get diversification analysis

**Example - Buy Stock:**
```bash
curl -X POST "http://localhost:8000/api/portfolio/buy" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d {
    "stock_symbol": "AAPL",
    "quantity": 10,
    "price": 150.50
  }
```

**Example - Get Portfolio Analysis:**
```bash
curl -X GET "http://localhost:8000/api/portfolio/analysis/overview" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 6. **AI Financial Strategy Advisor**
Conversational chatbot for personalized financial advice.

#### Endpoints:
- `POST /api/chat/conversations` - Create new conversation
- `GET /api/chat/conversations` - Get all your conversations
- `GET /api/chat/conversations/{conversation_id}` - Get specific conversation
- `POST /api/chat/conversations/{conversation_id}/messages` - Send message to AI
- `GET /api/chat/conversations/{conversation_id}/messages` - Get all messages

**Example - Create Conversation:**
```bash
curl -X POST "http://localhost:8000/api/chat/conversations" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**Example - Send Message:**
```bash
curl -X POST "http://localhost:8000/api/chat/conversations/conversation_id/messages" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d {
    "content": "How should I diversify my portfolio?"
  }
```

---

## 🧪 Quick Start Test

### 1. Register a user:
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@test.com","password":"test123"}'
```

### 2. Login to get token:
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```
Save the `access_token` from the response.

### 3. Get your profile:
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Make a prediction:
```bash
curl -X POST "http://localhost:8000/api/predictions/create" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"stock_symbol":"AAPL","user_prediction":"up","confidence_score":0.8,"reasoning":"Strong fundamentals"}'
```

### 5. Buy stocks:
```bash
curl -X POST "http://localhost:8000/api/portfolio/buy" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"stock_symbol":"AAPL","quantity":5,"price":150}'
```

### 6. Chat with AI advisor:
```bash
curl -X POST "http://localhost:8000/api/chat/conversations" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
Then use the returned `conversation_id` to send messages.

---

## 🗄️ Database Schema

The app uses SQLite with the following models:
- **User** - User accounts and profiles
- **LearningModule** - Finance learning content
- **UserLearningProgress** - Track learning progress
- **Assessment** - Learning assessments
- **UserAssessment** - Assessment submissions
- **Prediction** - Stock predictions
- **FinancialNews** - News articles with sentiment analysis
- **Portfolio** - User investment portfolios
- **PortfolioHolding** - Individual stocks in portfolio
- **Conversation** - Chat conversations
- **ConversationMessage** - Chat messages

Database file: `test.db`

---

## 📁 Project Structure

```
fin_ai/
├── __init__.py
├── main.py                 # FastAPI app
├── database.py            # Database config
├── auth.py                # Auth router (legacy)
├── utils.py               # Utility functions
├── core/
│   ├── __init__.py
│   └── security.py        # JWT, password hashing
├── models/
│   ├── __init__.py
│   └── models.py          # SQLAlchemy models
├── schemas/
│   ├── __init__.py
│   └── schemas.py         # Pydantic schemas
└── routes/
    ├── __init__.py
    ├── auth.py            # Auth endpoints
    ├── learning.py        # Learning endpoints
    ├── prediction.py      # Prediction endpoints
    ├── news.py            # News endpoints
    ├── portfolio.py       # Portfolio endpoints
    └── chat.py            # Chat endpoints
```

---

## 🔐 Security

- Passwords are hashed using bcrypt
- JWT tokens for authentication (60-minute expiry)
- OAuth2 with Bearer token scheme
- CORS enabled for frontend integration

---

## 🚀 Next Steps

1. **Connect Frontend**: Build a React/Vue frontend to consume these APIs
2. **Add Real Data**: Integrate with stock market APIs (Alpha Vantage, IEX, etc.)
3. **AI Integration**: Connect to OpenAI/LLaMA for advanced chatbot
4. **News Integration**: Add real-time news feeds from financial APIs
5. **Machine Learning**: Build ML models for stock predictions
6. **Deployment**: Deploy to AWS, Heroku, or DigitalOcean

---

## 📞 Support

For API documentation, visit: **http://localhost:8000/docs**

Enjoy using FinAI! 🎉
