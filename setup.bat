@echo off
echo ========================================
echo    Simple CRM System Setup
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo.

echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo 🚀 To start the CRM system, run:
echo    python app.py
echo.
echo 📱 Access the application at: http://localhost:5000
echo 👤 Login credentials: admin / admin123
echo.
echo 💡 The database will be automatically initialized on first run!
echo.
pause 