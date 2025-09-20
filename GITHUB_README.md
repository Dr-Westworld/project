# Legal Document Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 16+](https://img.shields.io/badge/node.js-16+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-red.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org/)

> **AI-powered Legal Document Assistant that demystifies legal documents and generates step-by-step progress paths with interactive nested stage cards.**

## 🎯 **What This Does**

Transform complex legal documents into clear, actionable progress paths with:
- **📄 Document Analysis** - Upload PDFs/Word docs for AI processing
- **🗺️ Progress Paths** - Generate step-by-step guides
- **🎴 Interactive Cards** - Nested stage cards with expandable details
- **💬 AI Chat** - Ask questions about your progress
- **🌐 Web Crawling** - Real-time legal source integration
- **🔍 Smart Search** - Vector-based document retrieval

## 🚀 **Quick Start**

### **Option 1: Docker (Recommended)**
```bash
# Clone the repository
git clone https://github.com/yourusername/legal-document-assistant.git
cd legal-document-assistant

# Run quick start script
chmod +x quick-start.sh
./quick-start.sh
# Choose option 1 for Docker

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### **Option 2: Manual Setup**
```bash
# Clone and setup
git clone https://github.com/yourusername/legal-document-assistant.git
cd legal-document-assistant

# Frontend
npm install
npm start

# Backend (new terminal)
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 📋 **Prerequisites**

- **Node.js 16+** - [Download](https://nodejs.org/)
- **Python 3.9+** - [Download](https://python.org/)
- **Docker** (Optional) - [Download](https://docker.com/)

### **API Keys Required**
- **OpenAI API Key** - [Get here](https://platform.openai.com/)
- **Pinecone Account** - [Sign up](https://www.pinecone.io/)
- **Google Cloud Account** - [Sign up](https://cloud.google.com/)

## 🏗️ **Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React UI      │    │   FastAPI       │    │   AI Services   │
│   - Stage Cards │◄──►│   - REST API    │◄──►│   - OpenAI      │
│   - Chat        │    │   - Auth        │    │   - Document AI │
│   - Upload      │    │   - Processing  │    │   - Web Crawler │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Vector Store  │
                    │   - Pinecone    │
                    │   - RAG Pipeline│
                    └─────────────────┘
```

## 🎨 **Key Features**

### **Interactive UI**
- **Nested Stage Cards** - Click to expand and see detailed sub-stages
- **Cross Button (❌)** - Minimize expanded views
- **Progress Tracking** - Mark stages as completed
- **Responsive Design** - Works on all devices

### **AI-Powered Processing**
- **Document AI** - Google Cloud integration for document analysis
- **Web Crawling** - Real-time legal source discovery
- **Vector Search** - Intelligent document retrieval
- **LLM Integration** - OpenAI GPT for progress generation

### **Developer Experience**
- **Complete API** - FastAPI with OpenAPI documentation
- **Docker Support** - Easy deployment and scaling
- **Testing Suite** - Comprehensive test coverage
- **Modern Python** - pyproject.toml configuration

## 📚 **Documentation**

- **[Developer Guide](DEVELOPER_GUIDE.md)** - Complete setup instructions
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs
- **[Project Summary](PROJECT_SUMMARY.md)** - Technical overview

## 🧪 **Testing**

```bash
# Run comprehensive tests
python test_complete_system.py

# Run individual tests
./test_system.sh

# Using pytest
pytest
```

## 🐳 **Docker Deployment**

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔧 **Configuration**

Copy `backend/env.example` to `backend/.env` and configure:

```env
# Required API Keys
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
GOOGLE_CLOUD_PROJECT_ID=your-project-id

# Optional Configuration
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

## 📁 **Project Structure**

```
legal-document-assistant/
├── src/                    # React frontend
├── backend/               # FastAPI backend
├── api/                   # API specification
├── docker-compose.yml     # Docker configuration
├── pyproject.toml        # Python packaging
└── README.md             # This file
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **Author**

**Om Gawade** - [gawade1420@gmail.com](mailto:gawade1420@gmail.com)

## 🙏 **Acknowledgments**

- Google Cloud AI services
- OpenAI for LLM capabilities
- Pinecone for vector storage
- React and FastAPI communities
- Open source contributors

---

## ⚡ **Quick Links**

- **[🚀 Quick Start](DEVELOPER_GUIDE.md#quick-start-for-developers)**
- **[🔧 Setup Guide](DEVELOPER_GUIDE.md#installation-methods)**
- **[📖 API Docs](http://localhost:8000/docs)**
- **[🐛 Issues](https://github.com/yourusername/legal-document-assistant/issues)**
- **[💬 Discussions](https://github.com/yourusername/legal-document-assistant/discussions)**

**Ready to demystify legal documents? Start with the Quick Start guide above! 🎉**
