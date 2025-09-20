@echo off
REM Legal Document Assistant - Complete Setup Script for Windows
echo 🚀 Setting up Legal Document Assistant - Complete System...
echo.

REM Colors for output (Windows doesn't support colors in batch, but we can use echo)
echo [INFO] Checking prerequisites...

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ first.
    echo Visit: https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.9+ first.
    echo Visit: https://python.org/
    pause
    exit /b 1
)

echo ✅ Node.js and Python are installed

REM Create project structure
echo [INFO] Creating project structure...
if not exist "backend\logs" mkdir backend\logs
if not exist "backend\uploads" mkdir backend\uploads
if not exist "backend\data" mkdir backend\data
if not exist "backend\crawler" mkdir backend\crawler
if not exist "backend\rag" mkdir backend\rag
if not exist "backend\services" mkdir backend\services
if not exist "src\components" mkdir src\components
if not exist "src\data" mkdir src\data
if not exist "public" mkdir public

echo ✅ Project structure created

REM Install frontend dependencies
echo [INFO] Installing frontend dependencies...
call npm install
if errorlevel 1 (
    echo ❌ Failed to install frontend dependencies
    pause
    exit /b 1
)

echo ✅ Frontend dependencies installed

REM Install Tailwind CSS
echo [INFO] Setting up Tailwind CSS...
call npm install -D tailwindcss postcss autoprefixer
call npx tailwindcss init -p

if errorlevel 1 (
    echo ⚠️  Tailwind CSS setup failed, but continuing...
) else (
    echo ✅ Tailwind CSS configured
)

REM Set up Python virtual environment
echo [INFO] Setting up Python virtual environment...
cd backend
python -m venv venv

if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment created

REM Activate virtual environment and install dependencies
echo [INFO] Installing backend dependencies...
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install backend dependencies
    pause
    exit /b 1
)

echo ✅ Backend dependencies installed

REM Install additional dependencies
echo [INFO] Installing additional dependencies...
pip install playwright beautifulsoup4 aiohttp

REM Install Playwright browsers
echo [INFO] Installing Playwright browsers...
playwright install

if errorlevel 1 (
    echo ⚠️  Playwright browser installation failed, but continuing...
) else (
    echo ✅ Playwright browsers installed
)

REM Create environment configuration
echo [INFO] Creating environment configuration...
if not exist ".env" (
    copy env.example .env
    echo ✅ Environment configuration created
) else (
    echo ✅ Environment configuration already exists
)

cd ..

REM Create Google Cloud setup script for Windows
echo [INFO] Creating Google Cloud setup script...
(
echo @echo off
echo echo 🔧 Setting up Google Cloud services...
echo.
echo REM Check if gcloud is installed
echo gcloud --version ^>nul 2^>^&1
echo if errorlevel 1 ^(
echo     echo ❌ Google Cloud CLI is not installed.
echo     echo Please install it from: https://cloud.google.com/sdk/docs/install
echo     pause
echo     exit /b 1
echo ^)
echo.
echo REM Check if user is authenticated
echo gcloud auth list --filter=status:ACTIVE --format="value(account)" ^| findstr . ^>nul 2^>^&1
echo if errorlevel 1 ^(
echo     echo 🔐 Please authenticate with Google Cloud:
echo     gcloud auth login
echo ^)
echo.
echo REM Set project
echo echo 📋 Please enter your Google Cloud Project ID:
echo set /p PROJECT_ID=Project ID: 
echo gcloud config set project %PROJECT_ID%
echo.
echo REM Enable required APIs
echo echo 🔌 Enabling required APIs...
echo gcloud services enable documentai.googleapis.com
echo gcloud services enable aiplatform.googleapis.com
echo gcloud services enable storage.googleapis.com
echo gcloud services enable run.googleapis.com
echo.
echo REM Create service account
echo echo 👤 Creating service account...
echo gcloud iam service-accounts create legal-assistant-sa --description="Service account for Legal Document Assistant" --display-name="Legal Assistant SA"
echo.
echo REM Grant necessary permissions
echo echo 🔑 Granting permissions...
echo gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:legal-assistant-sa@%PROJECT_ID%.iam.gserviceaccount.com" --role="roles/documentai.apiUser"
echo gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:legal-assistant-sa@%PROJECT_ID%.iam.gserviceaccount.com" --role="roles/aiplatform.user"
echo gcloud projects add-iam-policy-binding %PROJECT_ID% --member="serviceAccount:legal-assistant-sa@%PROJECT_ID%.iam.gserviceaccount.com" --role="roles/storage.admin"
echo.
echo REM Create and download key
echo echo 🔐 Creating service account key...
echo gcloud iam service-accounts keys create legal-assistant-key.json --iam-account=legal-assistant-sa@%PROJECT_ID%.iam.gserviceaccount.com
echo.
echo echo ✅ Google Cloud setup complete!
echo echo 📁 Service account key saved as: legal-assistant-key.json
echo echo 🔧 Update your .env file with the correct paths and project ID
echo pause
) > setup-google-cloud.bat

REM Create API keys setup script for Windows
echo [INFO] Creating API keys setup script...
(
echo @echo off
echo echo 🔑 Setting up API keys...
echo.
echo REM OpenAI API Key
echo echo Please enter your OpenAI API key:
echo set /p OPENAI_KEY=OpenAI API Key: 
echo if not "%%OPENAI_KEY%%"=="" ^(
echo     powershell -Command "^(Get-Content backend\.env^) -replace 'your-openai-api-key-here', '%%OPENAI_KEY%%' ^| Set-Content backend\.env"
echo     echo ✅ OpenAI API key configured
echo ^)
echo.
echo REM Pinecone API Key
echo echo Please enter your Pinecone API key:
echo set /p PINECONE_KEY=Pinecone API Key: 
echo if not "%%PINECONE_KEY%%"=="" ^(
echo     powershell -Command "^(Get-Content backend\.env^) -replace 'your-pinecone-api-key-here', '%%PINECONE_KEY%%' ^| Set-Content backend\.env"
echo     echo ✅ Pinecone API key configured
echo ^)
echo.
echo REM Generate random secrets
echo echo [INFO] Generating random secrets...
echo powershell -Command "$secret = -join ((1..32) ^| ForEach {Get-Random -InputObject @('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9')}; $secret"
echo set SECRET_KEY=
echo for /f %%i in ('powershell -Command "$secret = -join ((1..32) ^| ForEach {Get-Random -InputObject @('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9')}; $secret"') do set SECRET_KEY=%%i
echo powershell -Command "^(Get-Content backend\.env^) -replace 'your-secret-key-here-change-this-in-production', '%SECRET_KEY%' ^| Set-Content backend\.env"
echo.
echo for /f %%i in ('powershell -Command "$secret = -join ((1..32) ^| ForEach {Get-Random -InputObject @('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9')}; $secret"') do set JWT_SECRET=%%i
echo powershell -Command "^(Get-Content backend\.env^) -replace 'your-jwt-secret-key-here-change-this-in-production', '%JWT_SECRET%' ^| Set-Content backend\.env"
echo.
echo echo ✅ Random secrets generated and configured
echo echo 🎉 API keys setup complete!
echo pause
) > setup-api-keys.bat

REM Create startup script for Windows
echo [INFO] Creating startup script...
(
echo @echo off
echo echo 🚀 Starting Legal Document Assistant...
echo.
echo REM Start backend
echo echo Starting backend server...
echo cd backend
echo call venv\Scripts\activate
echo start "Backend Server" cmd /k "python main.py"
echo.
echo REM Wait a moment for backend to start
echo timeout /t 3 /nobreak ^>nul
echo.
echo REM Start frontend
echo echo Starting frontend server...
echo cd ..
echo start "Frontend Server" cmd /k "npm start"
echo.
echo echo ✅ Both servers are starting...
echo echo 🌐 Frontend: http://localhost:3000
echo echo 🔧 Backend API: http://localhost:8000
echo echo 📚 API Docs: http://localhost:8000/docs
echo echo.
echo echo Press any key to stop both servers
echo pause
echo.
echo echo Stopping servers...
echo taskkill /f /im node.exe ^>nul 2^>^&1
echo taskkill /f /im python.exe ^>nul 2^>^&1
echo echo Servers stopped.
) > start.bat

REM Create test script for Windows
echo [INFO] Creating test script...
(
echo @echo off
echo echo 🧪 Testing Legal Document Assistant system...
echo.
echo REM Test backend health
echo echo Testing backend health...
echo curl -s http://localhost:8000/health
echo if errorlevel 1 ^(
echo     echo ❌ Backend health check failed
echo ^) else ^(
echo     echo ✅ Backend health check passed
echo ^)
echo.
echo REM Test frontend
echo echo Testing frontend...
echo curl -s http://localhost:3000 ^| findstr "Legal Document Assistant" ^>nul
echo if errorlevel 1 ^(
echo     echo ❌ Frontend test failed
echo ^) else ^(
echo     echo ✅ Frontend is accessible
echo ^)
echo.
echo echo 🎉 System test complete!
) > test-system.bat

echo.
echo ✅ Setup complete! Here's what was created:
echo.
echo 📁 Project Structure:
echo   ├── Frontend (React + Tailwind)
echo   ├── Backend (FastAPI + AI Services)
echo   ├── Web Crawler (Scrapy + Playwright)
echo   ├── Vector Store (Pinecone)
echo   ├── RAG Pipeline (OpenAI + Custom)
echo   └── Document Processing (Google Cloud AI)
echo.
echo 🔧 Setup Scripts:
echo   ├── setup-complete.bat (this script)
echo   ├── setup-google-cloud.bat (Google Cloud setup)
echo   ├── setup-api-keys.bat (API keys configuration)
echo   ├── start.bat (start both servers)
echo   └── test-system.bat (test the system)
echo.
echo 📚 Documentation:
echo   ├── README.md (main documentation)
echo   ├── DEVELOPER_GUIDE.md (detailed setup guide)
echo   └── api/openapi.yaml (API specification)
echo.
echo 🚀 Next Steps:
echo   1. Run: setup-google-cloud.bat
echo   2. Run: setup-api-keys.bat
echo   3. Run: start.bat
echo   4. Open: http://localhost:3000
echo.
echo ✅ Legal Document Assistant setup complete! 🎉
pause
