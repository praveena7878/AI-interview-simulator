@echo off
echo ====================================================
echo   AI-Powered Adaptive Mock Interview System Launcher
echo ====================================================
echo.

cd /d "%~dp0"

echo [1/3] Setting up Python Backend...
cd backend
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)
call .venv\Scripts\activate
echo Installing backend requirements...
pip install -r requirements.txt
echo Starting Backend server...
start "AI Interview Backend" cmd /k "call .venv\Scripts\activate && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

cd /d "%~dp0"

echo [2/3] Setting up Frontend...
cd frontend
if not exist node_modules (
    echo Installing frontend dependencies...
    npm install
)
echo Starting Frontend dev server...
start "AI Interview Frontend" cmd /k "npm run dev"

echo [3/3] Opening browser...
timeout /t 5 >nul
start http://localhost:5173

echo.
echo ====================================================
echo   Servers launched! Feel free to close this window.
echo   - Backend runs at: http://localhost:8000
echo   - Frontend runs at: http://localhost:5173
echo ====================================================
pause
