#!/bin/bash

# Legal Document Assistant Setup Script
echo "🚀 Setting up Legal Document Assistant..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Node.js and Python are installed"

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Install Tailwind CSS
echo "🎨 Setting up Tailwind CSS..."
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Create backend virtual environment
echo "🐍 Setting up Python virtual environment..."
cd backend
python3 -m venv venv

# Activate virtual environment and install dependencies
echo "📦 Installing backend dependencies..."
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file for backend
echo "⚙️ Creating environment configuration..."
cat > .env << EOF
# Google Cloud Configuration
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Database Configuration (for production)
DATABASE_URL=sqlite:///./legal_assistant.db

# Security
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# AI Service Configuration
GOOGLE_GEMINI_API_KEY=your-gemini-api-key-here
GOOGLE_CLOUD_PROJECT_ID=your-project-id-here
EOF

cd ..

# Create directories
echo "📁 Creating necessary directories..."
mkdir -p logs
mkdir -p uploads
mkdir -p data

# Set permissions
echo "🔐 Setting up permissions..."
chmod +x setup.sh

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure your Google Cloud credentials in backend/.env"
echo "2. Start the backend server:"
echo "   cd backend && source venv/bin/activate && python main.py"
echo "3. Start the frontend server:"
echo "   npm start"
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "For detailed setup instructions, see README.md"
