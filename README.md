# Legal Document Assistant - Gen AI MVP

A comprehensive AI-powered application that demystifies legal documents and generates step-by-step progress paths. Users can upload legal documents, and the system will analyze them using Google AI features to create structured, interactive progress paths with detailed instructions.

## 🚀 Features

### Core Functionality
- **Document Upload**: Support for PDF and Word documents
- **AI-Powered Analysis**: Uses Google Cloud Document AI and Vertex AI for document processing
- **Progress Path Generation**: Creates structured, step-by-step progress paths
- **Interactive UI**: Nested stage cards with expandable detail views
- **Chat Interface**: AI-powered chat for questions and clarifications
- **Web Crawling**: Fetches authoritative legal sources for up-to-date information

### UI Features
- **Nested Stage Cards**: Rectangular cards representing each stage
- **Expandable Details**: Click any stage to see detailed sub-stages
- **Recursive Exploration**: Drill down into sub-stages with more details
- **Progress Tracking**: Mark stages as completed
- **Cross Button**: Minimize expanded views with ❌ button
- **Responsive Design**: Works on desktop and mobile devices

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

## 🛠️ Setup Instructions

### Prerequisites
- Node.js 16+ and npm
- Python 3.8+
- Google Cloud Platform account
- Git

### Frontend Setup

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Install Tailwind CSS**:
   ```bash
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   ```

3. **Start development server**:
   ```bash
   npm start
   ```

4. **Open browser**: Navigate to `http://localhost:3000`

### Backend Setup

1. **Create virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google Cloud credentials**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/service-account-key.json"
   ```

4. **Start the server**:
   ```bash
   python main.py
   ```

5. **API Documentation**: Visit `http://localhost:8000/docs`

### Google Cloud Setup

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
- Contact: support@legalassistant.com
- Documentation: [API Docs](http://localhost:8000/docs)

## 🙏 Acknowledgments

- Google Cloud AI services
- React and FastAPI communities
- Legal professionals who provided feedback
- Open source contributors

---

**Disclaimer**: This tool provides AI-generated assistance and should not be considered legal advice. Always consult with qualified legal professionals for important legal matters.
