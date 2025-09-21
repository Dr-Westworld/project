@echo off
REM Legal Document Assistant - Quick Start Script for Windows
REM This script helps developers get the application running quickly on Windows

echo.
echo 🚀 Legal Document Assistant - Quick Start
echo ==========================================
echo.

REM Check if we're in the right directory
if not exist "package.json" (
    echo ❌ Please run this script from the project root directory
    pause
    exit /b 1
)

if not exist "pyproject.toml" (
    echo ❌ Please run this script from the project root directory
    pause
    exit /b 1
)

echo [INFO] Welcome to Legal Document Assistant setup!
echo.
echo This script will help you get the application running quickly.
echo Choose your preferred setup method:
echo.
echo 1. Docker (Recommended - Easiest)
echo 2. Manual Setup (Development)
echo 3. Modern Python (pyproject.toml)
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto docker_setup
if "%choice%"=="2" goto manual_setup
if "%choice%"=="3" goto modern_python
if "%choice%"=="4" goto exit
echo ❌ Invalid choice. Please run the script again.
pause
exit /b 1

:docker_setup
echo.
echo [INFO] Setting up with Docker...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    echo Visit: https://docker.com/
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist "backend\.env" (
    echo [INFO] Creating environment configuration...
    copy backend\env.example backend\.env
    echo ⚠️  Please edit backend\.env with your API keys before continuing
    echo [INFO] Required: GOOGLE_GEMINI_API_KEY, PINECONE_API_KEY, GOOGLE_CLOUD_PROJECT_ID
    pause
)

REM Start Docker services
echo [INFO] Starting Docker services...
docker-compose up -d

if errorlevel 1 (
    echo ❌ Failed to start Docker services
    pause
    exit /b 1
)

echo.
echo ✅ Docker services started successfully!
echo.
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo [INFO] To stop the services: docker-compose down
goto end

:manual_setup
echo.
echo [INFO] Setting up manually...

REM Check prerequisites
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    echo Visit: https://nodejs.org/
    pause
    exit /b 1
)

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9+ first.
    echo Visit: https://python.org/
    pause
    exit /b 1
)

REM Frontend setup
echo [INFO] Setting up frontend...
call npm install
if errorlevel 1 (
    echo ❌ Frontend setup failed
    pause
    exit /b 1
)

call npm install -D tailwindcss postcss autoprefixer
call npx tailwindcss init -p

echo ✅ Frontend setup complete

REM Backend setup
echo [INFO] Setting up backend...
cd backend

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt
pip install playwright beautifulsoup4 aiohttp
playwright install

REM Create .env file
if not exist ".env" (
    copy env.example .env
    echo ⚠️  Please edit .env with your API keys
)

cd ..

echo ✅ Backend setup complete
echo.
echo [INFO] To start the application:
echo Terminal 1: npm start
echo Terminal 2: cd backend ^&^& venv\Scripts\activate ^&^& python main.py
goto end

:modern_python
echo.
echo [INFO] Setting up with modern Python (pyproject.toml)...

REM Check prerequisites
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    echo Visit: https://nodejs.org/
    pause
    exit /b 1
)

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9+ first.
    echo Visit: https://python.org/
    pause
    exit /b 1
)

REM Frontend setup
echo [INFO] Setting up frontend...
call npm install
call npm install -D tailwindcss postcss autoprefixer
call npx tailwindcss init -p

REM Backend setup
echo [INFO] Setting up backend with pyproject.toml...

REM Create virtual environment
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate

REM Install package in development mode
pip install -e ".[dev]"
playwright install

REM Create .env file
if not exist "backend\.env" (
    copy backend\env.example backend\.env
    echo ⚠️  Please edit backend\.env with your API keys
)

echo ✅ Setup complete with pyproject.toml
echo.
echo [INFO] To start the application:
echo Terminal 1: npm start
echo Terminal 2: python backend\main.py
goto end

:exit
echo [INFO] Exiting...
exit /b 0

:end
echo.
echo ✅ Setup complete! 🎉
echo.
echo [INFO] Next steps:
echo 1. Configure your API keys in backend\.env
echo 2. Start the application using the instructions above
echo 3. Open http://localhost:3000 in your browser
echo 4. Try the demo mode to see the nested stage cards!
echo.
echo [INFO] For detailed instructions, see DEVELOPER_GUIDE.md
pause
