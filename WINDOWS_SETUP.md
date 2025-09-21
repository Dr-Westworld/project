# Legal Document Assistant - Windows Setup Guide

## 🪟 **Windows-Specific Instructions**

This guide is specifically for Windows users who want to run the Legal Document Assistant on their Windows machine.

## 🚀 **Quick Start for Windows**

### **Option 1: One-Click Setup (Recommended)**
```cmd
# 1. Clone the repository
git clone https://github.com/yourusername/legal-document-assistant.git
cd legal-document-assistant

# 2. Run the Windows setup script
setup-complete.bat

# 3. Configure API keys
setup-api-keys.bat

# 4. Start the application
start.bat
```

### **Option 2: Interactive Setup**
```cmd
# 1. Clone the repository
git clone https://github.com/yourusername/legal-document-assistant.git
cd legal-document-assistant

# 2. Run interactive setup
quick-start.bat
# Choose your preferred setup method (Docker, Manual, or Modern Python)
```

## 📋 **Windows Prerequisites**

### **Required Software**
- **Windows 10/11** (64-bit recommended)
- **Node.js 16+** - [Download here](https://nodejs.org/)
- **Python 3.9+** - [Download here](https://python.org/)
- **Git for Windows** - [Download here](https://git-scm.com/)
- **PowerShell 5.1+** (usually pre-installed)

### **Optional Software**
- **Docker Desktop for Windows** - [Download here](https://docker.com/)
- **Visual Studio Code** - [Download here](https://code.visualstudio.com/)

## 🔧 **Windows-Specific Setup**

### **Method 1: Docker (Easiest for Windows)**
```cmd
# 1. Install Docker Desktop for Windows
# 2. Clone the repository
git clone https://github.com/yourusername/legal-document-assistant.git
cd legal-document-assistant

# 3. Configure environment
copy backend\env.example backend\.env
# Edit backend\.env with your API keys

# 4. Start with Docker
docker-compose up -d

# 5. Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### **Method 2: Manual Setup (Windows)**
```cmd
# 1. Clone the repository
git clone https://github.com/yourusername/legal-document-assistant.git
cd legal-document-assistant

# 2. Setup frontend
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# 3. Setup backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
pip install playwright beautifulsoup4 aiohttp
playwright install

# 4. Configure environment
copy env.example .env
# Edit .env with your API keys

# 5. Start the application
# Terminal 1: npm start
# Terminal 2: cd backend && venv\Scripts\activate && python main.py
```

### **Method 3: Modern Python (Windows)**
```cmd
# 1. Clone the repository
git clone https://github.com/yourusername/legal-document-assistant.git
cd legal-document-assistant

# 2. Setup frontend
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# 3. Setup backend with pyproject.toml
python -m venv venv
venv\Scripts\activate
pip install -e ".[dev]"
playwright install

# 4. Configure environment
copy backend\env.example backend\.env
# Edit backend\.env with your API keys

# 5. Start the application
# Terminal 1: npm start
# Terminal 2: python backend\main.py
```

## 🪟 **Windows-Specific Scripts**

### **Available Scripts**
- **`quick-start.bat`** - Interactive setup script
- **`setup-complete.bat`** - Complete automated setup
- **`setup-google-cloud.bat`** - Google Cloud configuration
- **`setup-api-keys.bat`** - API keys configuration
- **`start.bat`** - Start both frontend and backend
- **`test-system.bat`** - Test the system

### **Running Scripts**
```cmd
# Make sure you're in the project root directory
cd legal-document-assistant

# Run any script by double-clicking or using command prompt
quick-start.bat
setup-complete.bat
start.bat
test-system.bat
```

## 🔑 **API Keys Setup for Windows**

### **1. Google Gemini API Key**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign up or log in with your Google account
3. Click "Create API Key"
4. Copy your API key
5. Run `setup-api-keys.bat` and enter your key

### **2. Pinecone API Key**
1. Go to [Pinecone Console](https://app.pinecone.io/)
2. Sign up or log in
3. Go to API Keys section
4. Copy your API key
5. Run `setup-api-keys.bat` and enter your key

### **3. Google Cloud Setup**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Run `setup-google-cloud.bat` and follow the prompts
4. Download the service account key JSON file
5. Update `backend\.env` with the file path

## 🧪 **Testing on Windows**

### **Run Tests**
```cmd
# Test the system
test-system.bat

# Comprehensive Python tests
python test_complete_system.py

# Individual component tests
pytest
```

### **Manual Testing**
1. **Open Frontend**: http://localhost:3000
2. **View Demo**: Click "View Demo" to see nested stage cards
3. **Upload Document**: Click "Start Now" and upload a PDF/Word document
4. **Test Chat**: Use the chat interface to ask questions
5. **Test API**: Visit http://localhost:8000/docs for API documentation

## 🐛 **Windows Troubleshooting**

### **Common Windows Issues**

#### **PowerShell Execution Policy**
```powershell
# If you get execution policy errors, run this in PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### **Node.js Issues**
```cmd
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rmdir /s node_modules
del package-lock.json
npm install
```

#### **Python Issues**
```cmd
# Check Python version
python --version

# Recreate virtual environment
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### **Port Issues**
```cmd
# Check if ports are in use
netstat -an | findstr :3000
netstat -an | findstr :8000

# Kill processes using ports (if needed)
taskkill /f /im node.exe
taskkill /f /im python.exe
```

#### **Docker Issues**
```cmd
# Check Docker status
docker --version
docker-compose --version

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📁 **Windows File Structure**

```
legal-document-assistant/
├── src/                    # React frontend
├── backend/               # FastAPI backend
├── api/                   # API specification
├── *.bat                  # Windows batch scripts
├── *.sh                   # Unix/Linux shell scripts
├── docker-compose.yml     # Docker configuration
├── pyproject.toml        # Python packaging
└── README.md             # Main documentation
```

## 🚀 **Windows Development Workflow**

### **Making Changes**
1. **Frontend Changes**: Edit files in `src/` directory
2. **Backend Changes**: Edit files in `backend/` directory
3. **API Changes**: Update `api/openapi.yaml`

### **Code Quality (Windows)**
```cmd
# Format Python code
black backend/
isort backend/

# Format JavaScript code
npm run format

# Run linting
flake8 backend/
npm run lint
```

### **Git Workflow (Windows)**
```cmd
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add amazing feature"

# Push and create PR
git push origin feature/your-feature-name
```

## ✅ **Windows Success Checklist**

After following this guide, you should have:

- [ ] Frontend running on http://localhost:3000
- [ ] Backend running on http://localhost:8000
- [ ] API documentation accessible at http://localhost:8000/docs
- [ ] Demo mode working with nested stage cards
- [ ] Document upload functionality working
- [ ] Chat interface responding
- [ ] All tests passing

## 🎉 **You're Ready on Windows!**

Your Legal Document Assistant is now running on Windows! Start by exploring the demo mode to see the nested stage card functionality, then try uploading a real legal document to see the AI-powered progress path generation in action.

**Happy coding on Windows! 🪟🚀**
