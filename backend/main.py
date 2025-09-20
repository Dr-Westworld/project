from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uuid
import asyncio
from datetime import datetime
import json
import logging
import os
from pathlib import Path

# Import our custom services
from services.ai_service import AIService, create_ai_service
from document_processor import DocumentProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Legal Document Assistant API",
    description="API for processing legal documents and generating step-by-step progress paths using AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# In-memory storage for demo (replace with database in production)
plans_db = {}
documents_db = {}
chat_sessions = {}

# Pydantic models
class PlanResponse(BaseModel):
    planId: str
    status: str
    message: str
    estimatedProcessingTime: int

class Stage(BaseModel):
    id: str
    title: str
    shortDescription: str
    isCompleted: bool = False
    stageNumber: Optional[int] = None
    estimatedTime: Optional[str] = None
    requiredDocuments: Optional[List[str]] = None
    responsibleParty: Optional[str] = None
    dependencies: Optional[List[str]] = None
    confidence: Optional[str] = None
    citations: Optional[List[Dict[str, Any]]] = None
    website: Optional[str] = None
    warnings: Optional[List[str]] = None
    subStages: Optional[List['Stage']] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

class Plan(BaseModel):
    planId: str
    taskTitle: str
    status: str
    description: Optional[str] = None
    jurisdiction: Optional[str] = None
    documentType: Optional[str] = None
    stages: List[Stage]
    metadata: Optional[Dict[str, Any]] = None
    createdAt: datetime
    updatedAt: datetime

class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    messageId: str
    response: str
    suggestions: Optional[List[str]] = None
    relatedStages: Optional[List[str]] = None

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime

# Dependency for authentication (simplified for demo)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # In production, validate JWT token here
    return {"user_id": "demo_user", "email": "demo@example.com"}

# Mock AI service for document processing
class MockAIService:
    @staticmethod
    async def process_document(file_content: bytes, prompt: str, jurisdiction: str = None) -> Plan:
        """Mock document processing - replace with actual AI service"""
        await asyncio.sleep(2)  # Simulate processing time
        
        # Generate mock plan based on prompt
        plan_id = str(uuid.uuid4())
        now = datetime.now()
        
        # Sample plan structure
        stages = [
            Stage(
                id="stage_1",
                title="Create Government Account",
                shortDescription="Register on the official government portal",
                stageNumber=1,
                estimatedTime="30 minutes",
                requiredDocuments=["Government ID", "Email Address"],
                responsibleParty="user",
                confidence="high",
                website="https://portal.example.gov",
                citations=[
                    {
                        "url": "https://portal.example.gov/register",
                        "title": "Government Portal Registration",
                        "source_type": "government",
                        "excerpt": "Create your account to access government services"
                    }
                ],
                subStages=[
                    Stage(
                        id="stage_1_1",
                        title="Visit Registration Page",
                        shortDescription="Navigate to the registration page",
                        stageNumber=1,
                        estimatedTime="5 minutes",
                        responsibleParty="user",
                        confidence="high"
                    ),
                    Stage(
                        id="stage_1_2",
                        title="Fill Personal Information",
                        shortDescription="Enter your personal details",
                        stageNumber=2,
                        estimatedTime="10 minutes",
                        requiredDocuments=["Government ID"],
                        responsibleParty="user",
                        confidence="high"
                    ),
                    Stage(
                        id="stage_1_3",
                        title="Verify Email Address",
                        shortDescription="Click verification link in email",
                        stageNumber=3,
                        estimatedTime="5 minutes",
                        responsibleParty="user",
                        confidence="high"
                    )
                ],
                createdAt=now,
                updatedAt=now
            ),
            Stage(
                id="stage_2",
                title="Prepare Required Documents",
                shortDescription="Gather all necessary documentation",
                stageNumber=2,
                estimatedTime="2-3 hours",
                requiredDocuments=["Articles of Incorporation", "Operating Agreement", "Registered Agent Information"],
                responsibleParty="user",
                confidence="medium",
                citations=[
                    {
                        "url": "https://sos.ca.gov/business/llc/",
                        "title": "California LLC Requirements",
                        "source_type": "government",
                        "excerpt": "Required documents for LLC formation"
                    }
                ],
                warnings=["Ensure all documents are notarized", "Check for any state-specific requirements"],
                createdAt=now,
                updatedAt=now
            ),
            Stage(
                id="stage_3",
                title="Submit Application",
                shortDescription="File the incorporation documents",
                stageNumber=3,
                estimatedTime="1 hour",
                requiredDocuments=["Completed Application", "Filing Fee"],
                responsibleParty="user",
                confidence="high",
                website="https://bizfileonline.sos.ca.gov/",
                dependencies=["stage_1", "stage_2"],
                createdAt=now,
                updatedAt=now
            ),
            Stage(
                id="stage_4",
                title="Pay Filing Fees",
                shortDescription="Complete payment for incorporation",
                stageNumber=4,
                estimatedTime="15 minutes",
                requiredDocuments=["Payment Method"],
                responsibleParty="user",
                confidence="high",
                website="https://bizfileonline.sos.ca.gov/",
                dependencies=["stage_3"],
                createdAt=now,
                updatedAt=now
            )
        ]
        
        plan = Plan(
            planId=plan_id,
            taskTitle=f"Register LLC in {jurisdiction or 'California'}",
            status="ready",
            description=f"Step-by-step guide to register your LLC based on: {prompt}",
            jurisdiction=jurisdiction or "California, USA",
            documentType="incorporation",
            stages=stages,
            metadata={
                "totalStages": len(stages),
                "completedStages": 0,
                "estimatedTotalTime": "4-5 hours",
                "confidence": "high"
            },
            createdAt=now,
            updatedAt=now
        )
        
        return plan

    @staticmethod
    async def expand_stage(stage_id: str, context: str = "") -> Stage:
        """Mock stage expansion - replace with actual AI service"""
        await asyncio.sleep(1)  # Simulate processing time
        
        # Generate detailed sub-stages based on stage_id
        detailed_stage = Stage(
            id=stage_id,
            title=f"Detailed {stage_id.replace('_', ' ').title()}",
            shortDescription=f"Comprehensive breakdown of {stage_id}",
            description=f"This is a detailed explanation of {stage_id} with step-by-step instructions.",
            stageNumber=1,
            estimatedTime="2-3 hours",
            requiredDocuments=["Document A", "Document B"],
            responsibleParty="user",
            confidence="high",
            website="https://example.gov/instructions",
            citations=[
                {
                    "url": "https://example.gov/official-guide",
                    "title": "Official Government Guide",
                    "source_type": "government",
                    "excerpt": "Official instructions for this process"
                }
            ],
            warnings=["Important: Double-check all information before submitting"],
            subStages=[
                Stage(
                    id=f"{stage_id}_detail_1",
                    title="Step 1: Initial Preparation",
                    shortDescription="Gather preliminary information",
                    stageNumber=1,
                    estimatedTime="30 minutes",
                    responsibleParty="user",
                    confidence="high"
                ),
                Stage(
                    id=f"{stage_id}_detail_2",
                    title="Step 2: Document Review",
                    shortDescription="Review and verify all documents",
                    stageNumber=2,
                    estimatedTime="1 hour",
                    requiredDocuments=["Document A", "Document B"],
                    responsibleParty="user",
                    confidence="high"
                ),
                Stage(
                    id=f"{stage_id}_detail_3",
                    title="Step 3: Final Submission",
                    shortDescription="Submit the completed application",
                    stageNumber=3,
                    estimatedTime="30 minutes",
                    responsibleParty="user",
                    confidence="high"
                )
            ],
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
        
        return detailed_stage

    @staticmethod
    async def chat_response(plan_id: str, message: str, context: Dict[str, Any] = None) -> ChatResponse:
        """Mock chat response - replace with actual AI service"""
        await asyncio.sleep(1)  # Simulate processing time
        
        # Generate contextual response based on message
        response_text = f"I understand you're asking about: {message}. Based on your progress plan, here's what I recommend..."
        
        suggestions = [
            "What documents do I need for the next stage?",
            "How long will this process take?",
            "What are the common issues I should watch out for?"
        ]
        
        return ChatResponse(
            messageId=str(uuid.uuid4()),
            response=response_text,
            suggestions=suggestions,
            relatedStages=["stage_1", "stage_2"]
        )

# Initialize AI service
try:
    ai_service = create_ai_service()
    logger.info("AI service initialized successfully")
except Exception as e:
    logger.warning(f"Failed to initialize AI service: {str(e)}. Using mock service.")
    ai_service = MockAIService()

# API Endpoints
@app.post("/upload", response_model=PlanResponse)
async def upload_document(
    file: UploadFile = File(...),
    prompt: str = Form(...),
    jurisdiction: Optional[str] = Form(None),
    document_type: Optional[str] = Form("other"),
    current_user: dict = Depends(get_current_user)
):
    """Upload a legal document for processing"""
    try:
        # Validate file type
        if not file.content_type in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            raise HTTPException(
                status_code=415,
                detail="Unsupported file type. Please upload a PDF or Word document."
            )
        
        # Read file content
        file_content = await file.read()
        
        # Generate plan ID
        plan_id = str(uuid.uuid4())
        
        # Create uploads directory if it doesn't exist
        uploads_dir = Path("uploads")
        uploads_dir.mkdir(exist_ok=True)
        
        # Save file to disk
        file_path = uploads_dir / f"{plan_id}_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Store document metadata
        documents_db[plan_id] = {
            "filename": file.filename,
            "file_path": str(file_path),
            "content_type": file.content_type,
            "size": len(file_content),
            "uploaded_at": datetime.now(),
            "user_id": current_user["user_id"]
        }
        
        # Process document asynchronously
        asyncio.create_task(process_document_async(plan_id, str(file_path), prompt, jurisdiction))
        
        return PlanResponse(
            planId=plan_id,
            status="processing",
            message="Document uploaded successfully. Processing in progress...",
            estimatedProcessingTime=30
        )
        
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def process_document_async(plan_id: str, file_path: str, prompt: str, jurisdiction: str = None):
    """Process document asynchronously"""
    try:
        # Process document with AI service
        if hasattr(ai_service, 'process_document') and callable(getattr(ai_service, 'process_document')):
            # Use real AI service
            plan_data = await ai_service.process_document(file_path, prompt, jurisdiction)
        else:
            # Use mock service
            plan = await ai_service.process_document(file_path, prompt, jurisdiction)
            plan_data = plan.dict() if hasattr(plan, 'dict') else plan
        
        plan_data['planId'] = plan_id
        plan_data['status'] = 'ready'
        
        # Store plan in database
        plans_db[plan_id] = plan_data
        
        logger.info(f"Plan {plan_id} processed successfully")
        
    except Exception as e:
        logger.error(f"Error processing document {plan_id}: {str(e)}")
        # Store error status
        plans_db[plan_id] = {
            "planId": plan_id,
            "status": "failed",
            "error": str(e),
            "createdAt": datetime.now().isoformat()
        }

@app.get("/plans/{plan_id}", response_model=Plan)
async def get_plan(
    plan_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a progress plan"""
    if plan_id not in plans_db:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    plan_data = plans_db[plan_id]
    
    # Check if plan is still processing
    if plan_data.get("status") == "processing":
        return Plan(
            planId=plan_id,
            taskTitle="Processing...",
            status="processing",
            stages=[],
            createdAt=datetime.now(),
            updatedAt=datetime.now()
        )
    
    if plan_data.get("status") == "failed":
        raise HTTPException(status_code=500, detail="Plan processing failed")
    
    return Plan(**plan_data)

@app.get("/plans/{plan_id}/stages/{stage_id}", response_model=Stage)
async def get_stage_detail(
    plan_id: str,
    stage_id: str,
    expand_depth: int = 2,
    current_user: dict = Depends(get_current_user)
):
    """Get detailed information for a specific stage"""
    if plan_id not in plans_db:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Get plan data
    plan_data = plans_db[plan_id]
    
    # Find the stage in the plan
    stage_context = None
    for stage in plan_data.get('stages', []):
        if stage.get('id') == stage_id:
            stage_context = stage.get('title', '') + ' ' + stage.get('description', '')
            break
    
    if not stage_context:
        raise HTTPException(status_code=404, detail="Stage not found")
    
    # Get detailed stage information
    if hasattr(ai_service, 'expand_stage') and callable(getattr(ai_service, 'expand_stage')):
        # Use real AI service
        detailed_stage = await ai_service.expand_stage(
            stage_id, 
            stage_context, 
            plan_data.get('jurisdiction')
        )
    else:
        # Use mock service
        detailed_stage = await ai_service.expand_stage(stage_id)
    
    return detailed_stage

@app.post("/plans/{plan_id}/stages/{stage_id}/complete")
async def mark_stage_complete(
    plan_id: str,
    stage_id: str,
    completed: bool = True,
    notes: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Mark a stage as completed"""
    if plan_id not in plans_db:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Update stage completion status
    plan_data = plans_db[plan_id]
    if "stages" in plan_data:
        for stage in plan_data["stages"]:
            if stage["id"] == stage_id:
                stage["isCompleted"] = completed
                stage["updatedAt"] = datetime.now().isoformat()
                if notes:
                    stage["completionNotes"] = notes
                break
    
    return {
        "stageId": stage_id,
        "isCompleted": completed,
        "updatedAt": datetime.now().isoformat()
    }

@app.post("/plans/{plan_id}/chat", response_model=ChatResponse)
async def chat_with_plan(
    plan_id: str,
    chat_message: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    """Send a chat message about the plan"""
    if plan_id not in plans_db:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    # Generate chat response
    if hasattr(ai_service, 'chat_response') and callable(getattr(ai_service, 'chat_response')):
        # Use real AI service
        response = await ai_service.chat_response(
            plan_id, 
            chat_message.message, 
            chat_message.context
        )
    else:
        # Use mock service
        response = await ai_service.chat_response(
            plan_id, 
            chat_message.message, 
            chat_message.context
        )
    
    return response

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
