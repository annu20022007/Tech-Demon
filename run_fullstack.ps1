# PowerShell helper to build frontend and start backend in one command

# Navigate to frontend and build
Push-Location "FRONTEND\AI_POWERED_FINANCE_AND_INVESTMENT_SYSTEM\aiPoweredfinanceAndManagement"
Write-Host "Building frontend..."
npm install
$env:VITE_API_URL = "/api"
npm run build
Pop-Location

# Start backend (assumes virtual env already activated or dependencies installed)
Push-Location "BACKEND"
Write-Host "Starting backend server..."
uvicorn fin_ai.main:app --host 0.0.0.0 --port 8000
Pop-Location
