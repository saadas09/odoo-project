@echo off
echo ========================================
echo  Starting Mock API Server
echo  Hotel Reservation System
echo ========================================
echo.

cd /d "%~dp0"

echo Checking Python dependencies...
python -c "import fastapi, uvicorn, pydantic" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Required packages not installed!
    echo.
    echo Please run: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo Dependencies OK
echo.
echo Starting server on http://localhost:8000
echo Press CTRL+C to stop the server
echo.
echo ========================================
echo.

python -m uvicorn server:app --reload --port 8000

pause
