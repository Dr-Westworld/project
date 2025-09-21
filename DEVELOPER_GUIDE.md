# Legal Document Assistant - Developer Guide

## 🚀 **Quick Start for Developers**

This guide will help you get the Legal Document Assistant running on your machine from scratch, whether you're cloning from GitHub or starting fresh.

## 📋 **Prerequisites**

Before you begin, ensure you have the following installed:

### **Required Software**
- **Node.js 16+** - [Download here](https://nodejs.org/)
- **Python 3.9+** - [Download here](https://python.org/)
- **Git** - [Download here](https://git-scm.com/)
- **Docker** (Optional) - [Download here](https://docker.com/)

### **Windows Users**
- **PowerShell 5.1+** (usually pre-installed)
- **curl** (Windows 10+ has it built-in, or download from [here](https://curl.se/))

### **Required Accounts & API Keys**
- **Google Cloud Platform** account - [Sign up here](https://cloud.google.com/)
- **Google Gemini API Key** - [Get here](https://makersuite.google.com/app/apikey)
- **Pinecone Account** - [Sign up here](https://www.pinecone.io/)

## 🏗️ **Installation Methods**

Choose one of the following methods based on your preference:

---

## **Method 1: Quick Start Script (Easiest)**

### **For Windows Users**
```cmd
# 1. Clone the repository
git clone https://github.com/yourusername/legal-document-assistant.git
cd legal-document-assistant

# 2. Run quick start script
quick-start.bat
# Choose your preferred setup method

# 3. Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### **For Mac/Linux Users**
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/legal-document-assistant.git
cd legal-document-assistant

# 2. Run quick start script
chmod +x quick-start.sh
./quick-start.sh
# Choose your preferred setup method

# 3. Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

---

## **Method 2: Docker (Recommended - Easiest)**

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/yourusername/legal-document-assistant.git
cd legal-document-assistant
```

### **Step 2: Configure Environment Variables**
```bash
# Copy the environment template
cp backend/env.example backend/.env

# Edit the .env file with your API keys
nano backend/.env  # or use your preferred editor
```

**Required Environment Variables:**
```env
# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
GOOGLE_CLOUD_PROJECT_ID=your-project-id-here

# AI Service Configuration
GOOGLE_GEMINI_API_KEY=your-gemini-api-key-here
PINECONE_API_KEY=your-pinecone-api-key-here

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
```

### **Step 3: Start with Docker**
```bash
# Start all services
docker-compose up -d

# Check if services are running
docker-compose ps
```

### **Step 4: Access the Application**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### **Step 5: Stop the Application**
```bash
docker-compose down
```

---

## **Method 2: Manual Setup (Development)**

### **Step 1: Clone and Setup**
```bash
git clone https://github.com/yourusername/legal-document-assistant.git
cd legal-document-assistant
```

### **Step 2: Frontend Setup**
```bash
# Install Node.js dependencies
npm install

# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Start frontend (in a new terminal)
npm start
```

### **Step 3: Backend Setup**
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install additional dependencies
pip install playwright beautifulsoup4 aiohttp
playwright install

# Configure environment variables
cp env.example .env
# Edit .env with your API keys

# Start backend server
python main.py
```

### **Step 4: Access the Application**
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## **Method 3: Modern Python (pyproject.toml)**

### **Step 1: Clone and Setup**
```bash
git clone https://github.com/yourusername/legal-document-assistant.git
cd legal-document-assistant
```

### **Step 2: Frontend Setup**
```bash
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### **Step 3: Backend Setup with pyproject.toml**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the package in development mode
pip install -e ".[dev]"

# Install Playwright browsers
playwright install

# Configure environment
cp backend/env.example backend/.env
# Edit backend/.env with your API keys
```

### **Step 4: Run the Application**
```bash
# Terminal 1 - Frontend
npm start

# Terminal 2 - Backend
python backend/main.py
```

---

## 🔧 **Google Cloud Setup**

### **Step 1: Create Google Cloud Project**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Note your Project ID

### **Step 2: Enable Required APIs**
```bash
# Install Google Cloud CLI
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable documentai.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
```

### **Step 3: Create Service Account**
```bash
# Create service account
gcloud iam service-accounts create legal-assistant-sa \
    --description="Service account for Legal Document Assistant" \
    --display-name="Legal Assistant SA"

# Grant permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:legal-assistant-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/documentai.apiUser"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:legal-assistant-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Create and download key
gcloud iam service-accounts keys create legal-assistant-key.json \
    --iam-account=legal-assistant-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

### **Step 4: Update Environment Variables**
```env
GOOGLE_APPLICATION_CREDENTIALS=./legal-assistant-key.json
GOOGLE_CLOUD_PROJECT_ID=YOUR_PROJECT_ID
```

---

## 🔑 **API Keys Setup**

### **Google Gemini API Key**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign up or log in with your Google account
3. Click "Create API Key"
4. Copy your API key
5. Add to your `.env` file:
   ```env
   GOOGLE_GEMINI_API_KEY=your-gemini-api-key-here
   ```

### **Pinecone API Key**
1. Go to [Pinecone Console](https://app.pinecone.io/)
2. Sign up or log in
3. Go to API Keys section
4. Copy your API key
5. Add to your `.env` file:
   ```env
   PINECONE_API_KEY=your-pinecone-api-key-here
   ```

---

## 🧪 **Testing the Application**

### **Run Tests**

#### **For Windows Users**
```cmd
# Comprehensive system test
python test_complete_system.py

# Individual component tests
test-system.bat

# Using pytest (if using pyproject.toml)
pytest
```

#### **For Mac/Linux Users**
```bash
# Comprehensive system test
python test_complete_system.py

# Individual component tests
./test_system.sh

# Using pytest (if using pyproject.toml)
pytest
```

### **Manual Testing**
1. **Open Frontend**: http://localhost:3000
2. **View Demo**: Click "View Demo" to see the nested stage cards
3. **Upload Document**: Click "Start Now" and upload a PDF/Word document
4. **Test Chat**: Use the chat interface to ask questions
5. **Test API**: Visit http://localhost:8000/docs for API documentation

---

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Frontend Issues**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 16+
```

#### **Backend Issues**
```bash
# Check Python version
python --version  # Should be 3.9+

# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Check if ports are available
netstat -an | grep :3000  # Frontend port
netstat -an | grep :8000  # Backend port
```

#### **Docker Issues**
```bash
# Check Docker status
docker --version
docker-compose --version

# Rebuild containers
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Check logs
docker-compose logs backend
docker-compose logs frontend
```

#### **API Key Issues**
- Verify all API keys are correct in `.env` file
- Check if Google Cloud credentials file path is correct
 - Ensure Google Cloud project has Generative Language API enabled and you have an API key
- Verify Pinecone account is active

### **Logs and Debugging**
```bash
# Backend logs
tail -f backend/logs/legal_assistant.log

# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Check environment variables
python -c "import os; print(os.getenv('GOOGLE_GEMINI_API_KEY'))"
```

---

## 📁 **Project Structure**

```
legal-document-assistant/
├── src/                          # React frontend
│   ├── components/              # UI components
│   ├── data/                   # Sample data
│   └── App.jsx                 # Main app
├── backend/                     # FastAPI backend
│   ├── main.py                 # Main server
│   ├── services/               # AI services
│   ├── crawler/                # Web crawler
│   ├── rag/                    # RAG pipeline
│   └── requirements.txt        # Python dependencies
├── api/                        # API specification
│   └── openapi.yaml           # OpenAPI spec
├── docker-compose.yml          # Docker configuration
├── pyproject.toml             # Modern Python packaging
├── package.json               # Node.js dependencies
└── README.md                  # Main documentation
```

---

## 🚀 **Development Workflow**

### **Making Changes**
1. **Frontend Changes**: Edit files in `src/` directory
2. **Backend Changes**: Edit files in `backend/` directory
3. **API Changes**: Update `api/openapi.yaml`

### **Code Quality**
```bash
# Format Python code
black backend/
isort backend/

# Format JavaScript code
npm run format

# Run linting
flake8 backend/
npm run lint

# Type checking
mypy backend/
```

### **Git Workflow**
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add your feature"

# Push and create PR
git push origin feature/your-feature-name
```

---

## 📚 **Additional Resources**

### **Documentation**
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://reactjs.org/)
- [Google Cloud Document AI](https://cloud.google.com/document-ai)
- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Pinecone Documentation](https://docs.pinecone.io/)

### **Support**
- **Issues**: [GitHub Issues](https://github.com/yourusername/legal-document-assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/legal-document-assistant/discussions)
- **Email**: gawade1420@gmail.com

---

## ✅ **Success Checklist**

After following this guide, you should have:

- [ ] Frontend running on http://localhost:3000
- [ ] Backend running on http://localhost:8000
- [ ] API documentation accessible at http://localhost:8000/docs
- [ ] Demo mode working with nested stage cards
- [ ] Document upload functionality working
- [ ] Chat interface responding
- [ ] All tests passing

---

## 🎉 **You're Ready!**

Your Legal Document Assistant is now running! Start by exploring the demo mode to see the nested stage card functionality, then try uploading a real legal document to see the AI-powered progress path generation in action.

**Happy coding! 🚀**
