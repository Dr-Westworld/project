# Legal Document Assistant - Complete Gen AI MVP

A comprehensive AI-powered application that demystifies legal documents and generates step-by-step progress paths. Users can upload legal documents, and the system will analyze them using Google AI features to create structured, interactive progress paths with detailed instructions.

## 🎯 **COMPLETE SYSTEM OVERVIEW**

This is a **full-stack Gen AI MVP** that includes:
- ✅ **React Frontend** with nested stage cards and expandable detail views
- ✅ **FastAPI Backend** with complete API specification
- ✅ **Google Cloud Document AI** integration for document processing
- ✅ **Web Crawler** for authoritative legal sources
- ✅ **Vector Database & RAG Pipeline** for intelligent retrieval
- ✅ **OpenAI Integration** for LLM-powered responses
- ✅ **Docker Configuration** for easy deployment
- ✅ **Comprehensive Testing** suite

## 🚀 Features

### Core Functionality
- **Document Upload**: Support for PDF and Word documents
- **AI-Powered Analysis**: Uses Google Cloud Document AI and Vertex AI for document processing
- **Progress Path Generation**: Creates structured, step-by-step progress paths
- **Interactive UI**: Nested stage cards with expandable detail views
- **Chat Interface**: AI-powered chat for questions and clarifications
- **Web Crawling**: Fetches authoritative legal sources for up-to-date information
- **Vector Search**: RAG pipeline for intelligent document retrieval
- **Real-time Processing**: Async document processing with progress tracking

### UI Features
- **Nested Stage Cards**: Rectangular cards representing each stage
- **Expandable Details**: Click any stage to see detailed sub-stages
- **Recursive Exploration**: Drill down into sub-stages with more details
- **Progress Tracking**: Mark stages as completed
- **Cross Button (❌)**: Minimize expanded views as requested
- **Responsive Design**: Works on desktop and mobile devices
- **Demo Mode**: Interactive demo with sample data

## 🏗️ Architecture

### Frontend (React)
- **React 18** with functional components and hooks
- **Tailwind CSS** for styling and responsive design
- **Component Structure**:
  - `PlanView`: Main container component
  - `StageCard`: Reusable stage card component
  - `StageDetail`: Expanded detail view with sub-stages
  - `UploadArea`: Drag-and-drop file upload
  - `ChatInterface`: AI chat functionality

### Backend (FastAPI)
- **FastAPI** for high-performance API
- **OpenAPI 3.0** specification for API documentation
- **Authentication**: JWT-based authentication
- **File Processing**: Document parsing and analysis
- **AI Integration**: Google Cloud AI services

### AI Services
- **Document AI**: OCR and structured data extraction
- **Vertex AI**: LLM for plan generation and chat responses
- **Vector Search**: RAG pipeline for document retrieval
- **Web Crawler**: Scrapy + Playwright for legal source crawling

## 📁 Project Structure

```
legal-document-assistant/
├── src/                          # React frontend
│   ├── components/
│   │   ├── PlanView.jsx         # Main container
│   │   ├── StageCard.jsx        # Stage card component
│   │   ├── StageDetail.jsx      # Detailed stage view
│   │   ├── UploadArea.jsx       # File upload component
│   │   └── ChatInterface.jsx    # Chat component
│   ├── App.jsx                  # Main app component
│   ├── App.css                  # Custom styles
│   ├── index.js                 # React entry point
│   └── index.css                # Global styles
├── backend/                     # FastAPI backend
│   ├── main.py                  # Main API server
│   └── requirements.txt         # Python dependencies
├── api/
│   └── openapi.yaml            # API specification
├── public/                      # Static assets
├── package.json                 # Node.js dependencies
├── tailwind.config.js          # Tailwind configuration
└── README.md                   # This file
```

## 🚀 **QUICK START (Complete Setup)**

### **For Developers (GitHub Clone)**
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

**📚 [Complete Developer Guide](DEVELOPER_GUIDE.md) - Step-by-step instructions for developers**

### **Option 1: Automated Setup (Local Development)**
```bash
# 1. Run the complete setup script
chmod +x setup_complete.sh
./setup_complete.sh

# 2. Configure Google Cloud
./setup_google_cloud.sh

# 3. Configure API keys
./setup_api_keys.sh

# 4. Start the system
./start.sh
```

### **Option 2: Docker Setup**
```bash
# 1. Configure environment variables
cp backend/env.example backend/.env
# Edit backend/.env with your API keys

# 2. Start with Docker Compose
docker-compose up -d

# 3. Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### **Option 3: Manual Setup**

#### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Google Cloud Platform account
- OpenAI API key
- Pinecone account
- Git

#### Frontend Setup
```bash
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm start
```

#### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install playwright beautifulsoup4 aiohttp
playwright install
python main.py
```

#### Google Cloud Setup
1. **Enable APIs**:
   - Document AI API
   - Vertex AI API
   - Cloud Storage API
   - Cloud Run API

2. **Create service account** with required permissions

3. **Set up Document AI processors** for legal document processing

4. **Configure Vertex AI** for LLM integration

## 🎯 Usage

### Basic Workflow

1. **Upload Document**: Drag and drop or select a PDF/Word document
2. **Enter Prompt**: Describe what you need help with
3. **Generate Plan**: AI analyzes document and creates progress path
4. **Explore Stages**: Click on stage cards to see detailed instructions
5. **Track Progress**: Mark stages as completed
6. **Ask Questions**: Use chat interface for clarifications

### Example Prompts
- "I need to register my company in California"
- "Help me understand this contract and what I need to do"
- "I want to file a lawsuit, what's the process?"
- "How do I comply with these regulations?"

## 🔧 API Endpoints

### Document Processing
- `POST /upload` - Upload document for processing
- `GET /plans/{planId}` - Get generated progress plan

### Stage Management
- `GET /plans/{planId}/stages/{stageId}` - Get detailed stage information
- `POST /plans/{planId}/stages/{stageId}/complete` - Mark stage as completed

### Chat Interface
- `POST /plans/{planId}/chat` - Send chat message about plan

### System
- `GET /health` - Health check endpoint

## 🎨 UI Components

### Stage Cards
- **Visual Design**: Rectangular cards with color-coded levels
- **Interactive**: Click to expand and see details
- **Progress Indicators**: Show completion status
- **Responsive**: Adapt to different screen sizes

### Expandable Details
- **Nested Structure**: Sub-stages shown as smaller cards
- **Recursive**: Can drill down multiple levels
- **Close Button**: ❌ button to minimize expanded views
- **Rich Content**: Links, citations, warnings, and tips

### Chat Interface
- **Real-time**: Instant AI responses
- **Contextual**: Understands current progress
- **Suggestions**: Provides helpful follow-up questions

## 🔒 Security & Compliance

### Data Protection
- **Encryption**: All data encrypted in transit and at rest
- **Access Control**: JWT-based authentication
- **Privacy**: No data retention without consent

### Legal Compliance
- **Disclaimers**: Clear AI assistance disclaimers
- **Source Attribution**: All information properly cited
- **Human Review**: Encourages legal professional consultation

## 📊 Performance & Monitoring

### Metrics
- **Processing Time**: Document analysis speed
- **Accuracy**: Plan generation quality
- **User Engagement**: Stage completion rates
- **Error Rates**: System reliability

### Monitoring
- **Health Checks**: API endpoint monitoring
- **Error Tracking**: Comprehensive error logging
- **Performance**: Response time monitoring

## 🚀 Deployment

### Frontend (React)
```bash
npm run build
# Deploy build/ folder to your hosting service
```

### Backend (FastAPI)
```bash
# Using Docker
docker build -t legal-assistant-api .
docker run -p 8000:8000 legal-assistant-api

# Using Cloud Run
gcloud run deploy legal-assistant-api --source .
```

## 🧪 **Testing & Quality Assurance**

### **Automated Testing**
```bash
# Run comprehensive system tests
python test_complete_system.py

# Run individual component tests
./test_system.sh
```

### **Test Coverage**
- ✅ **Backend Health**: API endpoints and services
- ✅ **Frontend Accessibility**: UI components and navigation
- ✅ **Document Processing**: Upload and analysis pipeline
- ✅ **AI Integration**: LLM and vector store functionality
- ✅ **Web Crawler**: Legal source discovery and indexing
- ✅ **RAG Pipeline**: Retrieval and generation accuracy
- ✅ **API Documentation**: OpenAPI specification validation

### **Performance Testing**
- **Load Testing**: Concurrent user simulation
- **Document Processing**: Large file handling
- **Vector Search**: Query response times
- **Memory Usage**: Resource optimization

## 🔮 Future Enhancements

### Planned Features
- **Multi-language Support**: Support for multiple jurisdictions
- **Template Library**: Pre-built templates for common legal processes
- **Integration**: Connect with legal databases and court systems
- **Mobile App**: Native mobile application
- **Advanced AI**: More sophisticated document analysis

### Technical Improvements
- **Real-time Updates**: Live progress tracking
- **Collaboration**: Multi-user plan sharing
- **Export Options**: PDF, Word, and other formats
- **API Rate Limiting**: Production-ready rate limiting

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Contact:
- Documentation: 

## 🙏 Acknowledgments

- Google Cloud AI services
- React and FastAPI communities
- Legal professionals who provided feedback
- Open source contributors

---

**Disclaimer**: This tool provides AI-generated assistance and should not be considered legal advice. Always consult with qualified legal professionals for important legal matters.
