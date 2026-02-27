# Full Stack FinAI Application

This repository contains both the **backend** (FastAPI) and **frontend** (React + Vite) components for the AI-powered finance and investment system. The two parts are kept together so you can run a complete full‑stack application with a single command in production, or work on them separately during development.

---

## 🧱 Project Layout

```
BACKEND/     # Python FastAPI service
FRONTEND/    # React/Vite web client
```

The backend serves API endpoints under `/api/*`. In production the compiled frontend files are mounted at `/` so the entire app lives on one server.

---

## 🚀 Getting Started

### 1. Backend Setup

1. Navigate to the backend folder:
   ```powershell
   cd BACKEND
   ```
2. Create and activate a Python virtual environment (example using `venv`):
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. (Optional) populate the database or create tables:
   ```powershell
   python create_tables.py
   ```

### 2. Frontend Setup

1. Change into the frontend application:
   ```powershell
   cd ..\FRONTEND\AI_POWERED_FINANCE_AND_INVESTMENT_SYSTEM\aiPoweredfinanceAndManagement
   ```
2. Install Node modules:
   ```powershell
   npm install
   ```
3. Development server:
   ```powershell
   npm run dev
   ```
   Frontend will try to reach the API at `http://localhost:8000/api` by default (see `.env`).

### 3. Running During Development

- Start the backend with auto-reload:
  ```powershell
  cd BACKEND
  uvicorn fin_ai.main:app --reload --host 0.0.0.0 --port 8000
  ```
- In another terminal run the frontend with `npm run dev`.
- Use the web UI at `http://localhost:5173` (or whatever Vite reports) and the API at `http://localhost:8000/docs`.


the two services run independently; CORS is already enabled on the backend so the React client can call the endpoints.

### 4. Production Build / Single‑Server Deployment

1. Build the frontend:
   ```powershell
   cd FRONTEND\AI_POWERED_FINANCE_AND_INVESTMENT_SYSTEM\aiPoweredfinanceAndManagement
   npm run build
   ```
   Ensure `VITE_API_URL` is set to `/api` (the default after editing `.env`).

2. Start the backend normally (no need for a separate static server):
   ```powershell
   cd BACKEND
   uvicorn fin_ai.main:app --host 0.0.0.0 --port 8000
   ```

   FastAPI will serve the compiled frontend assets at `/`. Visiting `http://localhost:8000` now loads the React app; API calls go to `/api`.


---

## 📝 Additional Notes

- **Environment variables**: frontend uses `VITE_API_URL` during build and runtime; backend may use `.env` for secrets.
- **Tests**: backend contains unit tests under `BACKEND` (e.g. `test_*.py`). Run them using `pytest` from the backend folder.
- **CORS**: by default the backend allows all origins. You may restrict this for production.

---

With the configuration above, you're running a full-stack application from a single repository. Modify either layer as needed while preserving the communication contract over `/api`.
