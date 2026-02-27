# News-Based Stock Prediction System

## Overview

The prediction system has been **upgraded from basic dummy logic to an intelligent news-driven platform** that analyzes real market data and news sentiment to generate stock predictions.

## Architecture

### System Flow
```
User Creates Prediction Request
         ↓
[Fetch Latest News] ← NewsAPI
         ↓
[Analyze Sentiment] ← OpenAI LLM
         ↓
[Fetch Price Data] ← Alpha Vantage
         ↓
[Generate Prediction] ← Combined Signals
         ↓
[Store in Database] with News Context
         ↓
Return to User with Explanation
```

## Key Components

### 1. **News Fetching** (`fetch_news_for_stock`)
- Queries NewsAPI for the latest articles about the stock symbol
- Fetches top 10 most recent articles
- Filters by language (English) and relevance
- Returns title, content, source, and publication date

**Example:**
```bash
curl -X POST "http://localhost:8000/api/predictions/create" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "stock_symbol": "APPLE",
    "user_prediction": "up",
    "confidence_score": 0.7,
    "use_news_analysis": true
  }'
```

### 2. **Price Trend Analysis** (`fetch_price_data`)
- Fetches daily OHLC data from Alpha Vantage
- Analyzes last 5 days of price data
- Determines trend: `up`, `down`, or `neutral`
- Returns recent prices for context

**Trend Logic:**
- If latest close > oldest close → `UP`
- If latest close < oldest close → `DOWN`
- Otherwise → `NEUTRAL`

### 3. **News Sentiment Analysis** (`analyze_news_sentiment`)
- Uses OpenAI to understand news sentiment
- Prompts GPT with article headlines and sources
- Returns:
  - **Sentiment**: `positive`, `negative`, or `neutral`
  - **Confidence**: 0-100 (how certain is the analysis)
  - **Summary**: Market impact explanation
  - **Key Points**: Specific factors affecting the stock

**OpenAI Prompt:**
```
Analyze the sentiment of these recent news articles about {SYMBOL} stock and provide:
1. Overall sentiment (positive, negative, or neutral)
2. Confidence level (0-100)
3. Brief summary of market impact
4. Key points affecting stock price
```

### 4. **Intelligent Prediction Generation** (`generate_ai_prediction`)
- Combines news sentiment and price trend signals
- Uses weighted scoring:
  - **60% weight**: News sentiment from latest articles
  - **40% weight**: Recent price trend
- Generates prediction: `up`, `down`, or `neutral`
- Returns confidence score (0.0 - 0.95)

**Scoring Algorithm:**
```
sentiment_score = {positive: 100, neutral: 50, negative: 0}
trend_score = {up: 100, neutral: 50, down: 0}
combined_score = (sentiment_score × 0.6) + (trend_score × 0.4)

If combined_score ≥ 65 → PREDICT UP
If combined_score ≤ 35 → PREDICT DOWN
Otherwise → PREDICT NEUTRAL
```

### 5. **Database Storage**
Each prediction now stores:
- `news_sentiment` - analyzed sentiment from articles
- `price_trend` - recent price movement
- `related_news_ids` - URLs of articles used in analysis
- `prediction_factors` - detailed breakdown of decision
- `news_impact_score` - confidence in sentiment analysis
- `reasoning` - complete explanation with news context

## API Endpoints

### Create Prediction with News Analysis
```
POST /api/predictions/create
Content-Type: application/json
Authorization: Bearer {jwt_token}

{
  "stock_symbol": "TSLA",
  "user_prediction": "up",
  "confidence_score": 0.8,
  "use_news_analysis": true
}
```

**Response:**
```json
{
  "id": "pred_123",
  "stock_symbol": "TSLA",
  "user_prediction": "up",
  "ai_prediction": "up",
  "confidence_score": 0.85,
  "news_sentiment": "positive",
  "price_trend": "up",
  "news_impact_score": 78.5,
  "prediction_factors": "News Sentiment: positive (78.5% confidence)\nPrice Trend: up\nRecent Articles:\n- Tesla Q4 earnings exceed expectations\n\nKey Factors:\n• Strong delivery numbers\n• Positive analyst sentiment\n• Growing EV market demand",
  "reasoning": "Prediction based on: positive sentiment (78.5% confidence) from latest news + up price trend..."
}
```

### Get Prediction with News Context
```
GET /api/predictions/{prediction_id}
Authorization: Bearer {jwt_token}
```

Returns full prediction with all news analysis data.

### Evaluate Prediction & See News Impact
```
POST /api/predictions/{prediction_id}/evaluate
Authorization: Bearer {jwt_token}

{
  "actual_outcome": "up"
}
```

**Response Explanation:**
```
📊 AI Won! The AI's prediction of up was correct, while you predicted down. 
The news analysis and market data were key factors.

Reasoning: Prediction based on: positive sentiment (78.5% confidence) from 
latest news + up price trend. Tesla Q4 earnings exceed expectations...

📰 News Impact: The positive sentiment from recent news influenced the prediction.

Analysis Factors:
News Sentiment: positive (78.5% confidence)
Price Trend: up
Recent Articles:
- Tesla Q4 earnings exceed expectations

Key Factors:
• Strong delivery numbers
• Positive analyst sentiment
• Growing EV market demand
```

### View Statistics with News Metrics
```
GET /api/predictions/stats/overview
Authorization: Bearer {jwt_token}
```

**Response:**
```json
{
  "total_predictions": 15,
  "evaluated_predictions": 10,
  "user_correct": 6,
  "ai_correct": 8,
  "user_accuracy": 60.0,
  "ai_accuracy": 80.0,
  "news_based_predictions": 8,
  "news_based_accuracy": 87.5
}
```

## How News Influences Predictions

### Example 1: Positive News + Up Trend
```
Stock: NVDA
News: 5 articles about strong AI chip demand
Sentiment Analysis: positive (85% confidence)
Price Trend: up
Combined Score: (100 × 0.6) + (100 × 0.4) = 100
→ AI Prediction: UP with 85%+ confidence
```

### Example 2: Negative News + Down Trend
```
Stock: META
News: 3 articles about revenue miss and layoffs
Sentiment Analysis: negative (72% confidence)
Price Trend: down
Combined Score: (0 × 0.6) + (0 × 0.4) = 0
→ AI Prediction: DOWN with 72%+ confidence
```

### Example 3: Mixed Signals (Neutral)
```
Stock: MSFT
News: Mixed articles about new product launch delays vs. cloud growth
Sentiment Analysis: neutral (55% confidence)
Price Trend: stable
Combined Score: (50 × 0.6) + (50 × 0.4) = 50
→ AI Prediction: NEUTRAL with 50% confidence
```

## Data Flow Example

### User Creates Prediction
```
POST /api/predictions/create
{
  "stock_symbol": "AAPL",
  "user_prediction": "up",
  "use_news_analysis": true
}
```

### System Steps
1. **Fetch News** → NewsAPI returns 10 Apple articles
2. **Analyze Sentiment** → OpenAI determines "positive" (82% confidence)
3. **Price Data** → Alpha Vantage shows recent trend is "up"
4. **Generate Prediction** → Combined signals = 88 → Predict "UP"
5. **Store** → Database records:
   - news_sentiment: "positive"
   - price_trend: "up"
   - news_impact_score: 82.0
   - prediction_factors: [detailed breakdown]
6. **Return** → User sees AI prediction with confidence score

### User Evaluates Later (e.g., next day)
```
POST /api/predictions/{id}/evaluate
{
  "actual_outcome": "up"
}
```

### System Response
```
📊 AI Won! The AI's prediction of up was correct. 
The news analysis and market data were key factors.

News Impact: The positive sentiment from recent news influenced the prediction.
That article about Apple's strong iPhone sales was a key factor!
```

## API Keys Required

For full functionality, configure in `.env`:
```env
NEWSAPI_KEY=your_newsapi_key              # For news fetching
ALPHAVANTAGE_API_KEY=your_alphavantage    # For price data
OPENAI_API_KEY=your_openai_key            # For sentiment analysis
```

Without these:
- News fetching → Returns empty (uses neutral sentiment)
- Price data → Uses neutral trend
- Sentiment analysis → Falls back to neutral
- Prediction → Still works but with degraded intelligence

## Prediction Accuracy Metrics

The system tracks:
- **Total Predictions**: All predictions made
- **Evaluated Predictions**: Predictions checked against actual outcome
- **AI Accuracy**: % of AI predictions that were correct
- **News-Based Accuracy**: % of news-influenced predictions that were correct
- **User vs AI**: Compare your predictions against the AI

## Testing

Run the test script to see the system in action:
```bash
python test_news_prediction.py
```

This demonstrates:
1. Fetching news articles
2. Analyzing sentiment
3. Getting price trends
4. Generating predictions based on combined signals

## Future Enhancements

Potential improvements:
1. **More Data Sources**: Add earnings data, economic indicators, analyst ratings
2. **Advanced NLP**: Use VADER sentiment, named entity recognition for company mentions
3. **Machine Learning**: Train a model on historical news + price correlations
4. **Real-time Updates**: Web socket connections for live news impact
5. **Backtesting**: Test predictions against historical news + price data
6. **Explainability**: Show which specific news articles most influenced each prediction
7. **Risk Scoring**: Calculate Sharpe ratio and max drawdown recommendations

## Summary

The prediction system is now **fully integrated with real-time news data** and uses a weighted signal approach (60% news sentiment + 40% price trends) to generate intelligent stock predictions. Every prediction is backed by:
- Latest news articles from NewsAPI
- Sentiment analysis via OpenAI
- Price trend data from Alpha Vantage
- Detailed reasoning and analysis factors
- Transparent accuracy tracking
