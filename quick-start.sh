#!/bin/bash

# Legal Document Assistant - Quick Start Script
# This script helps developers get the application running quickly

echo "🚀 Legal Document Assistant - Quick Start"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check if we're in the right directory
if [ ! -f "package.json" ] || [ ! -f "pyproject.toml" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Welcome to Legal Document Assistant setup!"
echo ""
echo "This script will help you get the application running quickly."
echo "Choose your preferred setup method:"
echo ""
echo "1. Docker (Recommended - Easiest)"
echo "2. Manual Setup (Development)"
echo "3. Modern Python (pyproject.toml)"
echo "4. Exit"
echo ""

read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        print_status "Setting up with Docker..."
        
        # Check if Docker is installed
        if ! command -v docker &> /dev/null; then
            print_error "Docker is not installed. Please install Docker first."
            print_status "Visit: https://docker.com/"
            exit 1
        fi
        
        if ! command -v docker-compose &> /dev/null; then
            print_error "Docker Compose is not installed. Please install Docker Compose first."
            exit 1
        fi
        
        # Check if .env file exists
        if [ ! -f "backend/.env" ]; then
            print_status "Creating environment configuration..."
            cp backend/env.example backend/.env
            print_warning "Please edit backend/.env with your API keys before continuing"
            print_status "Required: GOOGLE_GEMINI_API_KEY, PINECONE_API_KEY, GOOGLE_CLOUD_PROJECT_ID"
            read -p "Press Enter after configuring your .env file..."
        fi
        
        # Start Docker services
        print_status "Starting Docker services..."
        docker-compose up -d
        
        if [ $? -eq 0 ]; then
            print_success "Docker services started successfully!"
            echo ""
            echo "🌐 Frontend: http://localhost:3000"
            echo "🔧 Backend: http://localhost:8000"
            echo "📚 API Docs: http://localhost:8000/docs"
            echo ""
            print_status "To stop the services: docker-compose down"
        else
            print_error "Failed to start Docker services"
            exit 1
        fi
        ;;
        
    2)
        print_status "Setting up manually..."
        
        # Check prerequisites
        if ! command -v node &> /dev/null; then
            print_error "Node.js is not installed. Please install Node.js 16+ first."
            exit 1
        fi
        
        if ! command -v python3 &> /dev/null; then
            print_error "Python 3 is not installed. Please install Python 3.9+ first."
            exit 1
        fi
        
        # Frontend setup
        print_status "Setting up frontend..."
        npm install
        npm install -D tailwindcss postcss autoprefixer
        npx tailwindcss init -p
        
        if [ $? -eq 0 ]; then
            print_success "Frontend setup complete"
        else
            print_error "Frontend setup failed"
            exit 1
        fi
        
        # Backend setup
        print_status "Setting up backend..."
        cd backend
        
        # Create virtual environment
        python3 -m venv venv
        
        # Activate virtual environment
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            source venv/Scripts/activate
        else
            source venv/bin/activate
        fi
        
        # Install dependencies
        pip install -r requirements.txt
        pip install playwright beautifulsoup4 aiohttp
        playwright install
        
        # Create .env file
        if [ ! -f ".env" ]; then
            cp env.example .env
            print_warning "Please edit .env with your API keys"
        fi
        
        cd ..
        
        print_success "Backend setup complete"
        echo ""
        print_status "To start the application:"
        echo "Terminal 1: npm start"
        echo "Terminal 2: cd backend && source venv/bin/activate && python main.py"
        ;;
        
    3)
        print_status "Setting up with modern Python (pyproject.toml)..."
        
        # Check prerequisites
        if ! command -v node &> /dev/null; then
            print_error "Node.js is not installed. Please install Node.js 16+ first."
            exit 1
        fi
        
        if ! command -v python3 &> /dev/null; then
            print_error "Python 3 is not installed. Please install Python 3.9+ first."
            exit 1
        fi
        
        # Frontend setup
        print_status "Setting up frontend..."
        npm install
        npm install -D tailwindcss postcss autoprefixer
        npx tailwindcss init -p
        
        # Backend setup
        print_status "Setting up backend with pyproject.toml..."
        
        # Create virtual environment
        python3 -m venv venv
        
        # Activate virtual environment
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            source venv/Scripts/activate
        else
            source venv/bin/activate
        fi
        
        # Install package in development mode
        pip install -e ".[dev]"
        playwright install
        
        # Create .env file
        if [ ! -f "backend/.env" ]; then
            cp backend/env.example backend/.env
            print_warning "Please edit backend/.env with your API keys"
        fi
        
        print_success "Setup complete with pyproject.toml"
        echo ""
        print_status "To start the application:"
        echo "Terminal 1: npm start"
        echo "Terminal 2: python backend/main.py"
        ;;
        
    4)
        print_status "Exiting..."
        exit 0
        ;;
        
    *)
        print_error "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
print_success "Setup complete! 🎉"
echo ""
print_status "Next steps:"
echo "1. Configure your API keys in backend/.env"
echo "2. Start the application using the instructions above"
echo "3. Open http://localhost:3000 in your browser"
echo "4. Try the demo mode to see the nested stage cards!"
echo ""
print_status "For detailed instructions, see DEVELOPER_GUIDE.md"
