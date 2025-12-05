@echo off
echo ========================================
echo  Installing Mock API Dependencies
echo  Hotel Reservation System
echo ========================================
echo.

cd /d "%~dp0"

echo Installing required packages:
echo   - fastapi
echo   - uvicorn  
echo   - pydantic
echo.

pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo  Installation completed successfully!
    echo ========================================
    echo.
    echo To start the mock API server, run:
    echo   start_server.bat
    echo.
) else (
    echo.
    echo ========================================
    echo  Installation failed!
    echo ========================================
    echo.
    echo Please check your Python and pip installation.
    echo.
)

pause
