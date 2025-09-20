@echo off
REM Legal Document Assistant - Test Script for Windows
echo 🧪 Testing Legal Document Assistant system...
echo.

REM Check if curl is available
curl --version >nul 2>&1
if errorlevel 1 (
    echo ❌ curl is not available. Please install curl or use Windows 10+ with curl.
    echo You can also test manually by opening:
    echo - Frontend: http://localhost:3000
    echo - Backend: http://localhost:8000
    echo - API Docs: http://localhost:8000/docs
    pause
    exit /b 1
)

REM Test backend health
echo [INFO] Testing backend health...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Backend health check failed
    echo [INFO] Make sure the backend server is running on port 8000
) else (
    echo ✅ Backend health check passed
)

REM Test frontend
echo [INFO] Testing frontend...
curl -s http://localhost:3000 | findstr "Legal Document Assistant" >nul 2>&1
if errorlevel 1 (
    echo ❌ Frontend test failed
    echo [INFO] Make sure the frontend server is running on port 3000
) else (
    echo ✅ Frontend is accessible
)

REM Test API documentation
echo [INFO] Testing API documentation...
curl -s http://localhost:8000/docs | findstr "FastAPI" >nul 2>&1
if errorlevel 1 (
    echo ❌ API documentation test failed
) else (
    echo ✅ API documentation is accessible
)

echo.
echo 🎉 System test complete!
echo.
echo [INFO] Manual testing:
echo 1. Open http://localhost:3000 in your browser
echo 2. Try the demo mode to see nested stage cards
echo 3. Upload a test document to see AI processing
echo 4. Use the chat interface to ask questions
echo.
pause
