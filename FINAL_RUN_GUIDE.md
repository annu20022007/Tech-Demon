# 🚀 FinAI Full-Stack App — Final Run Guide

Your **AI-powered Finance & Investment System** is a complete full-stack application:
- **Backend**: FastAPI (Python) on port **8001**
- **Frontend**: React/Vite on port **5174** (or 5173 if available)

---

## ✅ Quick Start

### **Development Mode (Recommended)**
Open **two separate terminals** and run these commands:

**Terminal 1 — Backend:**
```powershell
cd BACKEND
uvicorn fin_ai.main:app --reload --host 0.0.0.0 --port 8001
```

**Terminal 2 — Frontend:**
```powershell
cd FRONTEND\AI_POWERED_FINANCE_AND_INVESTMENT_SYSTEM\aiPoweredfinanceAndManagement
npm run dev
```

Then open your browser to:
- **Frontend**: `http://localhost:5173` (or `5174` if 5173 is busy)
- **API Docs**: `http://localhost:8001/docs`
- **Backend Health**: `http://localhost:8001/health`

### **Current Status**
Both services are now running:
- ✅ Backend listening on `0.0.0.0:8001`
- ✅ Frontend listening on `[::1]:5174` (Vite dev server)
- ✅ API reachable at `http://localhost:8001`
- ✅ UI reachable at `http://localhost:5174`

---

## 📋 What's Included

### **Backend Features** (http://localhost:8001)
- User authentication & profiles (JWT)
- Finance learning modules & assessments
- Stock prediction playground
- Financial news intelligence with sentiment analysis
- Market data & portfolio management
- Chat & advisory features
- Trading signals & predictions
- Background worker for async tasks

### **Frontend Features** (http://localhost:5174)
- Login/Registration
- Dashboard with insights
- Learning modules with quizzes
- Prediction arena (paper trading)
- Market news feed
- Portfolio management
- Real-time market data
- AI advisor chat

---

## 🛠️ Stopping Services

Press **Ctrl+C** in each terminal to stop the servers, or kill them by port:

```powershell
# Find and kill backend
netstat -ano | findstr :8001
taskkill /PID <pid> /F

# Find and kill frontend
netstat -ano | findstr :5173
taskkill /PID <pid> /F
```

---

## 🏗️ Production Build (Single Server)

To build and deploy as one server:

```powershell
# Build frontend
cd FRONTEND\AI_POWERED_FINANCE_AND_INVESTMENT_SYSTEM\aiPoweredfinanceAndManagement
$env:VITE_API_URL = "/api"
npm run build

# Start backend (serves compiled frontend + API)
cd ..\..\..
cd BACKEND
uvicorn fin_ai.main:app --host 0.0.0.0 --port 8001
```

Then visit `http://localhost:8001` — everything is served by FastAPI.

---

## 📝 Environment Variables

**Frontend** (`.env` in frontend folder):
```
VITE_API_URL=http://localhost:8001/api    # development
# VITE_API_URL=/api                        # production
```

**Backend** (create `.env` in BACKEND folder if needed for secrets):
```
DATABASE_URL=sqlite:///finai.db
SECRET_KEY=your-secret-key
```

---

## 🔍 Useful Endpoints

- `http://localhost:8001` — Backend home
- `http://localhost:8001/docs` — Swagger API documentation
- `http://localhost:8001/redoc` — ReDoc API documentation
- `http://localhost:8001/health` — Health check
- `http://localhost:5174` — Frontend React app

---

## 💡 Tips

1. **Port Conflicts?** If a port is busy:
   - Vite auto-selects the next port (5174, 5175, etc.)
   - Change backend port: `--port 8002`

2. **Auto-reload:** Both services watch for code changes and reload automatically during development.

3. **CORS:** Backend allows all origins for development. Restrict in production:
   - Edit `fin_ai/main.py` and change `allow_origins=["*"]`

4. **Database:** Backend uses SQLite by default at `BACKEND/finai.db`. Recreate tables:
   ```powershell
   cd BACKEND
   python create_tables.py
   ```

5. **Tests:** Run backend tests:
   ```powershell
   cd BACKEND
   pytest test_*.py
   ```

---

## 📦 Dependencies

**Backend Requirements** (in `BACKEND/requirements.txt`):
- FastAPI, Uvicorn
- SQLAlchemy, Pydantic
- JWT, bcrypt
- OpenAI, YFinance, NewsAPI, Alpha Vantage
- aiofiles (for static file serving)

**Frontend Dependencies** (in `FRONTEND/.../package.json`):
- React, React Router
- Tailwind CSS, Lucide React
- Recharts (charts), Framer Motion (animations)
- Axios, Vite

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: fin_ai` | Ensure you're in `BACKEND` folder before running uvicorn |
| `Port already in use` | Kill the process: `taskkill /PID <pid> /F` |
| `npm command not found` | Install Node.js from nodejs.org |
| `indicators.map is not a function` | Fixed! Check browser console for other errors |
| Backend/Frontend won't connect | Check `VITE_API_URL` in frontend `.env` matches backend port |
| Browser shows "site can't be reached" | Verify netstat shows LISTENING, try `127.0.0.1` instead of `localhost` |

---

## ✨ Next Steps

1. Both services should be **running and connected** now.
2. Open `http://localhost:5174` to use the app.
3. Create an account, explore the dashboard, and test features.
4. Modify code in either folder; services auto-reload.
5. For production, build with `npm run build` and deploy the single FastAPI server.

---

**Happy coding! 🎉**
