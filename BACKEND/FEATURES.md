# FinAI — Features & Frontend Design Guide

This document summarizes all backend features and maps them to UI pages/components, user flows, required APIs, and implementation notes so you can design the frontend.

---

## 1. High-level Product Areas

- Authentication & Profiles
- Finance Learning & Assessments
- Stock Prediction Playground (paper trading)
- Financial News Intelligence
- Portfolio Analyzer (paper portfolio)
- AI Financial Strategy Advisor (chatbot)
- Market Data & Charts
- Admin / Analytics (optional)

---

## 2. Main Pages & Components (Frontend)

1. Landing / Home
   - Hero, quick stats, call-to-action (Sign up / Login)
   - Links to Playground, Learning, Portfolio, News, Chat

2. Auth Flow
   - Sign up page (name, email, password)
   - Login page (email, password)
   - Forgot password (email) — backend placeholder
   - Profile page: view/edit name, bio, avatar, email

3. Dashboard (after login)
   - Key metrics: portfolio value, prediction accuracy, recent news
   - Quick actions: make prediction, open chat, buy/sell

4. Learning Center
   - Modules list (cards) with difficulty and progress bars
   - Module detail page: content, videos, resources, take assessment
   - Progress page: module progress, completed modules, badges
   - Assessment UI: questions, submit answers, show score

5. Prediction Playground
   - Create prediction modal/form: symbol, direction (up/down/neutral), confidence, reasoning
   - My predictions list: status, AI prediction, actual outcome, score, explanation
   - Prediction detail: timeline, explanation, compare user vs AI
   - Leaderboard (optional): best predictors

6. Market Data / Charting
   - Ticker search/autocomplete
   - Chart component: OHLC, volume, timeframe selector (1D, 1W, 1M, 1Y)
   - Price summary card: open/high/low/close, market cap (if available)
   - Small sparkline components for lists

7. News & Intelligence
   - News feed: cards with headline, source, time, sentiment tag
   - News detail: article text, related symbols, sentiment & impact explanation
   - Filters: symbol, sentiment, impact

8. Portfolio Analyzer (Paper Trading)
   - Portfolio overview: total value, cash, return, allocation pie chart
   - Holdings table: symbol, qty, avg cost, current price, P/L
   - Buy/Sell modal: enter qty/price, confirm trade (paper-only)
   - Analysis: diversification, risk exposure, time-series P/L

9. AI Strategy Advisor (Chat)
   - Conversation list (side panel) with last message preview
   - Chat window: message list, input box, attachments (optional)
   - Quick prompts: portfolio advice, news analysis, prediction insights
   - Conversation export / save

10. Settings & Integrations
    - API keys (if user-level API features exist)
    - Notifications preferences
    - Account settings

11. Admin (optional)
    - User management, content management for learning modules, system logs

---

## 3. UI Components & Patterns

- Authenticated header with user menu and quick actions
- Reusable Card component for modules, news, prediction items
- Modal forms for create actions (prediction, buy/sell)
- Table with pagination for holdings, predictions, news
- Responsive layout: grid on desktop, stacked on mobile
- Toast notifications for success/errors
- Charts: use Chart.js, Recharts or Highcharts (time-series + pie)
- Loading skeletons for API calls

---

## 4. API Endpoints (Backend → Frontend mapping)

Authentication
- POST `/api/auth/register` — register
- POST `/api/auth/login` — login (returns JWT)
- GET `/api/auth/me` — current user profile
- PUT `/api/auth/me` — update profile

Learning
- GET `/api/learning/modules` — list modules
- GET `/api/learning/progress` — user progress
- POST `/api/learning/modules/{id}/complete` — mark complete
- GET `/api/learning/modules/{id}/assessments` — module assessments
- POST `/api/learning/assessments/{id}/submit` — submit answers

Predictions (Playground)
- POST `/api/predictions/create` — create prediction
- GET `/api/predictions/my-predictions` — list user predictions
- GET `/api/predictions/{id}` — prediction details
- POST `/api/predictions/{id}/evaluate` — evaluate with actual outcome
- GET `/api/predictions/stats/overview` — prediction stats

Market Data
- GET `/api/market/daily/{symbol}` — daily time series (Alpha Vantage)

News
- GET `/api/news/search?q=...` — external news search
- GET `/api/news/` — local news list
- GET `/api/news/{id}` — news detail
- GET `/api/news/trending/stocks` — trending symbols

Portfolio
- GET `/api/portfolio/` — portfolio overview
- POST `/api/portfolio/buy` — buy (paper)
- POST `/api/portfolio/sell` — sell (paper)
- GET `/api/portfolio/analysis/overview` — analytics
- GET `/api/portfolio/analysis/diversification` — diversification

Chat / AI Advisor
- POST `/api/chat/conversations` — create conversation
- GET `/api/chat/conversations` — list conversations
- GET `/api/chat/conversations/{id}` — conversation details
- POST `/api/chat/conversations/{id}/messages` — send message (calls OpenAI)
- GET `/api/chat/conversations/{id}/messages` — get messages

---

## 5. Auth & Data Flow Notes

- All `POST`/private endpoints require `Authorization: Bearer <token>` header. Store JWT in secure storage (HTTP-only cookie recommended, or secure localStorage with refresh flow).
- Use optimistic UI updates for buy/sell and prediction creation; revert on error.
- Charts and live data: keep caching/backoff strategy to avoid API rate limits.

---

## 6. External Services Required (for full features)

- OpenAI (`OPENAI_API_KEY`) — chatbot & explanations
- Alpha Vantage (`ALPHAVANTAGE_API_KEY`) — market time series
- NewsAPI or Finnhub (`NEWSAPI_KEY` / `FINNHUB_API_KEY`) — news feed
- Polygon / IEX / yfinance — optional for richer market data

If keys are missing, frontend should show clear UI states: "Market data unavailable — enable API key".

---

## 7. Suggested Frontend Routes (React/Vue)

- `/` — landing
- `/login`, `/register`
- `/dashboard`
- `/learning` (list), `/learning/:id`
- `/playground` — prediction creation & list
- `/market/:symbol` — market chart
- `/news` (list), `/news/:id`
- `/portfolio`
- `/chat` and `/chat/:conversationId`
- `/settings`

---

## 8. UX Recommendations

- Start users with an onboarding: create profile, add mock portfolio, try prediction tutorial
- Use progressive disclosure for advanced features (paper trading, chat insights)
- Show API usage/billing warnings if OpenAI/AlphaVantage calls fail due to quota
- Provide export options (CSV/PDF) for portfolio and predictions

---

## 9. Accessibility & Performance

- Ensure color contrast and keyboard navigation
- Lazy-load heavy charts and images
- Paginate large lists and use server-side filtering
- Debounce search inputs (ticker/news)

---

## 10. Developer Notes

- JWT token stored client-side: prefer HTTP-only cookies for security
- Respect rate limits for Alpha Vantage (use caching)
- Mock endpoints exist for demo mode — toggle via `YFINANCE_FALLBACK` or `USE_MOCK_DATA`

---

## 11. Next Steps for Frontend

1. Build wireframes for Dashboard, Playground, Learning, Portfolio, and Chat.
2. Implement authentication and token storage.
3. Integrate chart library and design reusable data cards.
4. Implement API error handling and empty states.
5. Implement conversation UI tied to `/api/chat` endpoints.

---

If you want, I can also: generate example React component skeletons, create Storybook stories for the main components, or provide Figma-ready component lists. Tell me which you'd like next.
