@echo off
REM Mini Office local launcher.

title Mini Office - Local Launcher
color 0B

echo.
echo    MINI OFFICE - LOCAL REVIEW
echo.

echo [1/4] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python 3.8+ was not found.
    echo Install Python from https://python.org and retry.
    echo.
    pause
    exit /b 1
)
echo Python detected.

echo.
echo [2/4] Preparing virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Existing virtual environment detected.
)

echo.
echo [3/4] Activating environment...
call venv\Scripts\activate.bat

echo.
echo [4/4] Installing dependencies if requirements.txt exists...
if exist "requirements.txt" (
    pip install -r requirements.txt --quiet
    echo Dependencies installed.
) else (
    echo requirements.txt not found; continuing with local static app.
)

echo.
echo Launching Mini Office at http://127.0.0.1:8000
echo Press Ctrl+C in this window to stop the local server.
echo.

if exist "mini_office.py" (
    python mini_office.py
) else if exist "index.html" (
    start index.html
) else (
    echo ERROR: mini_office.py or index.html not found.
    pause
    exit /b 1
)

echo.
pause
