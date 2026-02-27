from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import auth, learning, prediction, news, portfolio, chat, market, dashboard, advisor
from .routes import trading
from .services.background import start_background_worker, stop_background_worker

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FinAI Backend",
    description="AI-powered Financial Learning & Trading Platform",
    version="1.0.0",
)

# CORS middleware (add BEFORE routes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes FIRST (important: must be before static files)
app.include_router(auth.router, prefix="/api")
app.include_router(learning.router, prefix="/api")
app.include_router(prediction.router, prefix="/api")
app.include_router(news.router, prefix="/api")
app.include_router(portfolio.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(advisor.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(market.router, prefix="/api")
app.include_router(trading.router, prefix="/api")

# Serve built frontend LAST (as catch-all for unmatched routes)
# Important: This must be AFTER all API routes are registered
# NOTE: Only mount in production when dist exists. In development, 
# the React app runs on port 5173 separately, so don't mount here.
from fastapi.staticfiles import StaticFiles
from pathlib import Path

frontend_dist = Path(__file__).resolve().parents[2] / "FRONTEND" / "AI_POWERED_FINANCE_AND_INVESTMENT_SYSTEM" / "aiPoweredfinanceAndManagement" / "dist"
# Uncomment below ONLY for production builds (when all files are in dist/)
# if frontend_dist.exists():
#     app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="frontend")


@app.get("/")
def home():
    return {
        "message": "FinAI Backend Running",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.on_event("startup")
def _startup():
    try:
        start_background_worker()
        print("Background worker started")
    except Exception as e:
        print("Failed to start background worker:", e)


@app.on_event("shutdown")
def _shutdown():
    try:
        stop_background_worker()
        print("Background worker stopped")
    except Exception as e:
        print("Failed to stop background worker:", e)
