@echo off
REM Legal Document Assistant - Start Script for Windows
echo 🚀 Starting Legal Document Assistant...
echo.

REM Check if we're in the right directory
if not exist "package.json" (
    echo ❌ Please run this script from the project root directory
    pause
    exit /b 1
)

REM Start backend
echo [INFO] Starting backend server...
cd backend

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup-complete.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment and start backend
call venv\Scripts\activate
start "Backend Server" cmd /k "python main.py"

REM Wait a moment for backend to start
echo [INFO] Waiting for backend to start...
timeout /t 3 /nobreak >nul

REM Start frontend
echo [INFO] Starting frontend server...
cd ..
start "Frontend Server" cmd /k "npm start"

echo.
echo ✅ Both servers are starting...
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo [INFO] The application will open in your default browser.
echo [INFO] Press any key to stop both servers
echo.

REM Open browser
start http://localhost:3000

REM Wait for user input
pause

echo.
echo [INFO] Stopping servers...
taskkill /f /im node.exe >nul 2>&1
taskkill /f /im python.exe >nul 2>&1
echo ✅ Servers stopped.
pause
