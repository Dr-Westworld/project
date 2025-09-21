#!/bin/bash

# Complete Legal Document Assistant Setup Script
echo "🚀 Setting up Legal Document Assistant - Complete System..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 16+ first."
    print_status "Visit: https://nodejs.org/"
    exit 1
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    print_status "Visit: https://python.org/"
    exit 1
fi

# Check pip
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3 first."
    exit 1
fi

print_success "Prerequisites check passed"

# Create project structure
print_status "Creating project structure..."
mkdir -p backend/logs
mkdir -p backend/uploads
mkdir -p backend/data
mkdir -p backend/crawler
mkdir -p backend/rag
mkdir -p backend/services
mkdir -p src/components
mkdir -p src/data
mkdir -p public

print_success "Project structure created"

# Install frontend dependencies
print_status "Installing frontend dependencies..."
npm install

if [ $? -eq 0 ]; then
    print_success "Frontend dependencies installed"
else
    print_error "Failed to install frontend dependencies"
    exit 1
fi

# Install Tailwind CSS
print_status "Setting up Tailwind CSS..."
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

if [ $? -eq 0 ]; then
    print_success "Tailwind CSS configured"
else
    print_warning "Tailwind CSS setup failed, but continuing..."
fi

# Set up Python virtual environment
print_status "Setting up Python virtual environment..."
cd backend
python3 -m venv venv

if [ $? -eq 0 ]; then
    print_success "Virtual environment created"
else
    print_error "Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment and install dependencies
print_status "Installing Python dependencies..."
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Upgrade pip first
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    print_success "Python dependencies installed"
else
    print_error "Failed to install Python dependencies"
    exit 1
fi

# Install additional dependencies for web crawling
print_status "Installing additional dependencies..."
pip install playwright beautifulsoup4 aiohttp

# Install Playwright browsers
print_status "Installing Playwright browsers..."
playwright install

if [ $? -eq 0 ]; then
    print_success "Playwright browsers installed"
else
    print_warning "Playwright browser installation failed, but continuing..."
fi

cd ..

# Create environment configuration
print_status "Creating environment configuration..."
cp backend/env.example backend/.env

print_success "Environment configuration created"

# Create Google Cloud setup script
print_status "Creating Google Cloud setup script..."
cat > setup_google_cloud.sh << 'EOF'
#!/bin/bash

echo "🔧 Setting up Google Cloud services..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI is not installed."
    echo "Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "🔐 Please authenticate with Google Cloud:"
    gcloud auth login
fi

# Set project
echo "📋 Please enter your Google Cloud Project ID:"
read -p "Project ID: " PROJECT_ID
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔌 Enabling required APIs..."
gcloud services enable documentai.googleapis.com
gcloud services enable aiplatform.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable run.googleapis.com

# Create service account
echo "👤 Creating service account..."
gcloud iam service-accounts create legal-assistant-sa \
    --description="Service account for Legal Document Assistant" \
    --display-name="Legal Assistant SA"

# Grant necessary permissions
echo "🔑 Granting permissions..."
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:legal-assistant-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/documentai.apiUser"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:legal-assistant-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:legal-assistant-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Create and download key
echo "🔐 Creating service account key..."
gcloud iam service-accounts keys create legal-assistant-key.json \
    --iam-account=legal-assistant-sa@$PROJECT_ID.iam.gserviceaccount.com

echo "✅ Google Cloud setup complete!"
echo "📁 Service account key saved as: legal-assistant-key.json"
echo "🔧 Update your .env file with the correct paths and project ID"
EOF

chmod +x setup_google_cloud.sh

# Create API keys setup script
print_status "Creating API keys setup script..."
cat > setup_api_keys.sh << 'EOF'
#!/bin/bash

echo "🔑 Setting up API keys..."

# Google Gemini API Key
echo "Please enter your Google Gemini API key:"
read -p "Google Gemini API Key: " GEMINI_KEY
if [ ! -z "$GEMINI_KEY" ]; then
    sed -i "s/your-gemini-api-key-here/$GEMINI_KEY/g" backend/.env
    echo "✅ Google Gemini API key configured"
fi

# Pinecone API Key
echo "Please enter your Pinecone API key:"
read -p "Pinecone API Key: " PINECONE_KEY
if [ ! -z "$PINECONE_KEY" ]; then
    sed -i "s/your-pinecone-api-key-here/$PINECONE_KEY/g" backend/.env
    echo "✅ Pinecone API key configured"
fi

# Generate random secrets
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET=$(openssl rand -hex 32)

sed -i "s/your-secret-key-here-change-this-in-production/$SECRET_KEY/g" backend/.env
sed -i "s/your-jwt-secret-key-here-change-this-in-production/$JWT_SECRET/g" backend/.env

echo "✅ Random secrets generated and configured"
echo "🎉 API keys setup complete!"
EOF

chmod +x setup_api_keys.sh

# Create startup script
print_status "Creating startup script..."
cat > start.sh << 'EOF'
#!/bin/bash

echo "🚀 Starting Legal Document Assistant..."

# Start backend
echo "Starting backend server..."
cd backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend server..."
cd ..
npm start &
FRONTEND_PID=$!

echo "✅ Both servers are starting..."
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
wait
EOF

chmod +x start.sh

# Create test script
print_status "Creating test script..."
cat > test_system.sh << 'EOF'
#!/bin/bash

echo "🧪 Testing Legal Document Assistant system..."

# Test backend health
echo "Testing backend health..."
curl -s http://localhost:8000/health | jq .

if [ $? -eq 0 ]; then
    echo "✅ Backend health check passed"
else
    echo "❌ Backend health check failed"
fi

# Test frontend
echo "Testing frontend..."
curl -s http://localhost:3000 | grep -q "Legal Document Assistant"

if [ $? -eq 0 ]; then
    echo "✅ Frontend is accessible"
else
    echo "❌ Frontend test failed"
fi

echo "🎉 System test complete!"
EOF

chmod +x test_system.sh

# Create Docker configuration
print_status "Creating Docker configuration..."
cat > Dockerfile << 'EOF'
# Multi-stage build for Legal Document Assistant

# Backend stage
FROM python:3.9-slim as backend

WORKDIR /app/backend

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ .

# Frontend stage
FROM node:16-alpine as frontend

WORKDIR /app/frontend

# Copy package files
COPY package*.json ./
COPY tailwind.config.js ./

# Install dependencies
RUN npm ci --only=production

# Copy frontend code
COPY src/ ./src/
COPY public/ ./public/

# Build frontend
RUN npm run build

# Final stage
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy backend
COPY --from=backend /app/backend ./backend

# Copy frontend build
COPY --from=frontend /app/frontend/build ./frontend/build

# Copy nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port
EXPOSE 80

# Start services
CMD ["sh", "-c", "cd backend && python main.py & nginx -g 'daemon off;'"]
EOF

cat > nginx.conf << 'EOF'
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server localhost:8000;
    }

    server {
        listen 80;
        server_name localhost;

        # Frontend
        location / {
            root /app/frontend/build;
            index index.html;
            try_files $uri $uri/ /index.html;
        }

        # Backend API
        location /api/ {
            proxy_pass http://backend/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
EOF

print_success "Docker configuration created"

# Create comprehensive README
print_status "Creating comprehensive documentation..."
cat > SETUP_GUIDE.md << 'EOF'
# Legal Document Assistant - Complete Setup Guide

## 🎯 Overview

This guide will help you set up the complete Legal Document Assistant system with all components:
- React frontend with nested stage cards
- FastAPI backend with AI integration
- Google Cloud Document AI for document processing
- Web crawler for legal sources
- Vector database and RAG pipeline
 - Google Gemini integration for LLM responses

## 🚀 Quick Start

### 1. Run the Setup Script
```bash
chmod +x setup_complete.sh
./setup_complete.sh
```

### 2. Configure Google Cloud
```bash
./setup_google_cloud.sh
```

### 3. Configure API Keys
```bash
./setup_api_keys.sh
```

### 4. Start the System
```bash
./start.sh
```

## 📋 Manual Setup

### Prerequisites
- Node.js 16+
- Python 3.8+
- Google Cloud account
- Google Gemini API key
- Pinecone account

### Frontend Setup
```bash
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

### Backend Setup
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install playwright beautifulsoup4 aiohttp
playwright install
```

### Environment Configuration
Copy `backend/env.example` to `backend/.env` and configure:
- Google Cloud credentials
- Google Gemini API key (set `GOOGLE_GEMINI_API_KEY`)
- Pinecone API key
- Database settings

## 🔧 Configuration

### Google Cloud Setup
1. Create a Google Cloud project
2. Enable required APIs:
   - Document AI API
   - Vertex AI API
   - Cloud Storage API
3. Create a service account with necessary permissions
4. Download the service account key JSON file

- **Pinecone**: Get from https://www.pinecone.io/
- **Google Cloud**: Create service account and download key
### API Keys
- **Google Gemini (Generative AI)**: Get an API key from Google Cloud Console and enable the Generative Language API
- **Pinecone**: Get from https://www.pinecone.io/
- **Google Cloud**: Create service account and download key
- **Pinecone**: Get from https://www.pinecone.io/
- **Google Cloud**: Create service account and download key

## 🏗️ Architecture

### Components
- **Frontend**: React with Tailwind CSS
- **Backend**: FastAPI with async support
- **Document Processing**: Google Cloud Document AI
- **Web Crawling**: Scrapy + Playwright
- **Vector Store**: Pinecone
- **LLM**: Google Gemini (Gemini Pro or appropriate model)
- **RAG Pipeline**: Custom implementation

### Data Flow
1. User uploads document
2. Document AI processes and extracts text
3. Web crawler gathers legal sources
4. Vector store indexes content
5. RAG pipeline generates progress path
6. Frontend displays nested stage cards

## 🧪 Testing

### Run Tests
```bash
./test_system.sh
```

### Manual Testing
1. Start the system: `./start.sh`
2. Open http://localhost:3000
3. Upload a sample document
4. Test the nested stage card functionality

## 🐳 Docker Deployment

### Build and Run
```bash
docker build -t legal-assistant .
docker run -p 80:80 legal-assistant
```

### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_GEMINI_API_KEY=${GOOGLE_GEMINI_API_KEY}
      - PINECONE_API_KEY=${PINECONE_API_KEY}
  
  frontend:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

## 🔍 Troubleshooting

### Common Issues
1. **Google Cloud credentials**: Ensure the JSON file path is correct
2. **API keys**: Verify all API keys are valid and have proper permissions
3. **Port conflicts**: Check if ports 3000 and 8000 are available
4. **Python dependencies**: Ensure virtual environment is activated

### Logs
- Backend logs: `backend/logs/legal_assistant.log`
- Frontend logs: Check browser console
- System logs: `./start.sh` output

## 📚 API Documentation

Once running, visit:
- API Docs: http://localhost:8000/docs
- OpenAPI Spec: http://localhost:8000/openapi.json

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check this setup guide
2. Review the logs
3. Create an issue in the repository
4. Contact the development team

---

**Happy coding! 🎉**
EOF

print_success "Comprehensive documentation created"

# Final summary
print_status "Setup complete! Here's what was created:"
echo ""
echo "📁 Project Structure:"
echo "  ├── Frontend (React + Tailwind)"
echo "  ├── Backend (FastAPI + AI Services)"
echo "  ├── Web Crawler (Scrapy + Playwright)"
echo "  ├── Vector Store (Pinecone)"
echo "  ├── RAG Pipeline (Google Gemini + Custom)"
echo "  └── Document Processing (Google Cloud AI)"
echo ""
echo "🔧 Setup Scripts:"
echo "  ├── setup_complete.sh (this script)"
echo "  ├── setup_google_cloud.sh (Google Cloud setup)"
echo "  ├── setup_api_keys.sh (API keys configuration)"
echo "  ├── start.sh (start both servers)"
echo "  └── test_system.sh (test the system)"
echo ""
echo "📚 Documentation:"
echo "  ├── README.md (main documentation)"
echo "  ├── SETUP_GUIDE.md (detailed setup guide)"
echo "  └── api/openapi.yaml (API specification)"
echo ""
echo "🚀 Next Steps:"
echo "  1. Run: ./setup_google_cloud.sh"
echo "  2. Run: ./setup_api_keys.sh"
echo "  3. Run: ./start.sh"
echo "  4. Open: http://localhost:3000"
echo ""
print_success "Legal Document Assistant setup complete! 🎉"
