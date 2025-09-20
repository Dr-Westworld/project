"""
Document Processor using Google Cloud Document AI
Handles PDF and Word document processing with OCR and structured extraction
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
import json
import os
from pathlib import Path
from datetime import datetime
import base64

# Google Cloud imports
from google.cloud import documentai
from google.cloud import storage
from google.oauth2 import service_account
import google.auth

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Processes legal documents using Google Cloud Document AI"""
    
    def __init__(self, google_cloud_project: str = None, credentials_path: str = None):
        """
        Initialize Document AI processor
        
        Args:
            google_cloud_project: Google Cloud project ID
            credentials_path: Path to service account credentials JSON
        """
        self.project_id = google_cloud_project or os.getenv('GOOGLE_CLOUD_PROJECT_ID')
        self.credentials_path = credentials_path or os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        self.location = "us"  # Document AI location
        self.processor_id = None
        self.processor_name = None
        
        # Initialize clients
        self.documentai_client = None
        self.storage_client = None
        
        self._initialize_clients()
        self._setup_processor()
    
    def _initialize_clients(self):
        """Initialize Google Cloud clients"""
        try:
            # Set up credentials
            if self.credentials_path and os.path.exists(self.credentials_path):
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
            else:
                # Use default credentials
                credentials, _ = google.auth.default()
            
            # Initialize Document AI client
            self.documentai_client = documentai.DocumentProcessorServiceClient(
                credentials=credentials
            )
            
            # Initialize Storage client
            self.storage_client = storage.Client(
                project=self.project_id,
                credentials=credentials
            )
            
            logger.info("Google Cloud clients initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Google Cloud clients: {str(e)}")
            raise
    
    def _setup_processor(self):
        """Set up Document AI processor"""
        try:
            # For demo purposes, we'll use a mock processor
            # In production, you would create a processor in the Google Cloud Console
            self.processor_id = "mock-processor-id"
            self.processor_name = f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}"
            
            logger.info(f"Document AI processor set up: {self.processor_name}")
            
        except Exception as e:
            logger.error(f"Error setting up processor: {str(e)}")
            # For demo purposes, continue with mock processor
            self.processor_id = "mock-processor-id"
            self.processor_name = f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}"
    
    async def process_document(self, file_path: str) -> Optional[Dict[str, Any]]:
        """
        Process a document using Document AI
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Dictionary containing extracted document data
        """
        try:
            logger.info(f"Processing document: {file_path}")
            
            # Read document file
            with open(file_path, "rb") as file:
                file_content = file.read()
            
            # For demo purposes, use mock processing
            # In production, this would use the actual Document AI API
            if self.processor_id == "mock-processor-id":
                return await self._mock_process_document(file_path, file_content)
            
            # Real Document AI processing
            return await self._real_process_document(file_content)
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            return None
    
    async def _mock_process_document(self, file_path: str, file_content: bytes) -> Dict[str, Any]:
        """Mock document processing for demo purposes"""
        try:
            # Simulate processing time
            await asyncio.sleep(2)
            
            # Extract basic information
            file_name = Path(file_path).name
            file_size = len(file_content)
            
            # Mock extracted text (in production, this would come from Document AI)
            mock_text = f"""
            This is a mock legal document: {file_name}
            
            Document Analysis:
            - File size: {file_size} bytes
            - Document type: Legal Contract/Agreement
            - Key entities detected: Company names, dates, monetary amounts
            - Important clauses: Liability, termination, payment terms
            
            This mock processing simulates what would be extracted by Google Cloud Document AI
            including OCR text, entity extraction, form field detection, and document structure.
            """
            
            # Mock structured data
            mock_entities = [
                {"type": "PERSON", "value": "John Doe", "confidence": 0.95},
                {"type": "ORGANIZATION", "value": "ABC Corporation", "confidence": 0.90},
                {"type": "MONEY", "value": "$50,000", "confidence": 0.88},
                {"type": "DATE", "value": "2024-01-15", "confidence": 0.92}
            ]
            
            mock_tables = [
                {
                    "headers": ["Item", "Description", "Amount"],
                    "rows": [
                        ["Legal Fees", "Contract review and preparation", "$2,500"],
                        ["Filing Fees", "State registration fees", "$500"],
                        ["Total", "", "$3,000"]
                    ]
                }
            ]
            
            return {
                "text": mock_text,
                "entities": mock_entities,
                "tables": mock_tables,
                "metadata": {
                    "file_name": file_name,
                    "file_size": file_size,
                    "processed_at": datetime.now().isoformat(),
                    "processor_id": self.processor_id,
                    "confidence_score": 0.85
                },
                "pages": [
                    {
                        "page_number": 1,
                        "text": mock_text,
                        "entities": mock_entities,
                        "tables": mock_tables
                    }
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in mock document processing: {str(e)}")
            return None
    
    async def _real_process_document(self, file_content: bytes) -> Dict[str, Any]:
        """Real Document AI processing (for production use)"""
        try:
            # Create document object
            document = documentai.Document(
                content=file_content,
                mime_type="application/pdf"  # or "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
            
            # Create process request
            request = documentai.ProcessRequest(
                name=self.processor_name,
                document=document
            )
            
            # Process document
            result = self.documentai_client.process_document(request=request)
            document = result.document
            
            # Extract text
            text = document.text
            
            # Extract entities
            entities = []
            for entity in document.entities:
                entities.append({
                    "type": entity.type_,
                    "value": entity.mention_text,
                    "confidence": entity.confidence
                })
            
            # Extract tables
            tables = []
            for page in document.pages:
                for table in page.tables:
                    table_data = self._extract_table_data(table, document.text)
                    tables.append(table_data)
            
            # Extract form fields
            form_fields = []
            for page in document.pages:
                for form_field in page.form_fields:
                    form_fields.append({
                        "field_name": form_field.field_name.text if form_field.field_name else "",
                        "field_value": form_field.field_value.text if form_field.field_value else "",
                        "confidence": form_field.field_name.confidence if form_field.field_name else 0.0
                    })
            
            return {
                "text": text,
                "entities": entities,
                "tables": tables,
                "form_fields": form_fields,
                "metadata": {
                    "processed_at": datetime.now().isoformat(),
                    "processor_id": self.processor_id,
                    "confidence_score": self._calculate_confidence_score(document)
                },
                "pages": [
                    {
                        "page_number": i + 1,
                        "text": page.text,
                        "entities": [e for e in entities if e.get("page_number") == i + 1],
                        "tables": [t for t in tables if t.get("page_number") == i + 1]
                    }
                    for i, page in enumerate(document.pages)
                ]
            }
            
        except Exception as e:
            logger.error(f"Error in real document processing: {str(e)}")
            return None
    
    def _extract_table_data(self, table, document_text: str) -> Dict[str, Any]:
        """Extract data from a table"""
        try:
            headers = []
            rows = []
            
            for row in table.body_rows:
                row_data = []
                for cell in row.cells:
                    cell_text = self._get_text_from_layout(cell.layout, document_text)
                    row_data.append(cell_text)
                rows.append(row_data)
            
            # Extract headers if available
            if table.header_rows:
                for row in table.header_rows:
                    header_data = []
                    for cell in row.cells:
                        cell_text = self._get_text_from_layout(cell.layout, document_text)
                        header_data.append(cell_text)
                    headers.extend(header_data)
            
            return {
                "headers": headers,
                "rows": rows
            }
            
        except Exception as e:
            logger.error(f"Error extracting table data: {str(e)}")
            return {"headers": [], "rows": []}
    
    def _get_text_from_layout(self, layout, document_text: str) -> str:
        """Extract text from layout element"""
        try:
            if layout.text_anchor:
                start_index = layout.text_anchor.text_segments[0].start_index
                end_index = layout.text_anchor.text_segments[0].end_index
                return document_text[start_index:end_index]
            return ""
        except Exception as e:
            logger.error(f"Error extracting text from layout: {str(e)}")
            return ""
    
    def _calculate_confidence_score(self, document) -> float:
        """Calculate overall confidence score for the document"""
        try:
            # Simple confidence calculation based on entity confidences
            if not document.entities:
                return 0.5
            
            total_confidence = sum(entity.confidence for entity in document.entities)
            return total_confidence / len(document.entities)
            
        except Exception as e:
            logger.error(f"Error calculating confidence score: {str(e)}")
            return 0.5
    
    async def process_document_from_url(self, gcs_uri: str) -> Optional[Dict[str, Any]]:
        """
        Process document from Google Cloud Storage URI
        
        Args:
            gcs_uri: Google Cloud Storage URI (gs://bucket/path)
            
        Returns:
            Dictionary containing extracted document data
        """
        try:
            # Create document object with GCS URI
            document = documentai.Document(
                input_config=documentai.DocumentInputConfig(
                    gcs_source=documentai.GcsSource(uri=gcs_uri)
                )
            )
            
            # Create process request
            request = documentai.ProcessRequest(
                name=self.processor_name,
                document=document
            )
            
            # Process document
            result = self.documentai_client.process_document(request=request)
            document = result.document
            
            # Extract and return data (same as real_process_document)
            return await self._extract_document_data(document)
            
        except Exception as e:
            logger.error(f"Error processing document from URL: {str(e)}")
            return None
    
    async def _extract_document_data(self, document) -> Dict[str, Any]:
        """Extract data from processed document"""
        try:
            # Extract text
            text = document.text
            
            # Extract entities
            entities = []
            for entity in document.entities:
                entities.append({
                    "type": entity.type_,
                    "value": entity.mention_text,
                    "confidence": entity.confidence
                })
            
            # Extract tables
            tables = []
            for page in document.pages:
                for table in page.tables:
                    table_data = self._extract_table_data(table, document.text)
                    tables.append(table_data)
            
            return {
                "text": text,
                "entities": entities,
                "tables": tables,
                "metadata": {
                    "processed_at": datetime.now().isoformat(),
                    "processor_id": self.processor_id,
                    "confidence_score": self._calculate_confidence_score(document)
                }
            }
            
        except Exception as e:
            logger.error(f"Error extracting document data: {str(e)}")
            return None

# Example usage
async def main():
    """Example usage of the document processor"""
    # Initialize processor
    processor = DocumentProcessor(
        google_cloud_project="your-project-id",
        credentials_path="path/to/credentials.json"
    )
    
    # Process a document
    result = await processor.process_document("sample_contract.pdf")
    
    if result:
        print("Document processed successfully:")
        print(f"Text length: {len(result['text'])}")
        print(f"Entities found: {len(result['entities'])}")
        print(f"Tables found: {len(result['tables'])}")
    else:
        print("Failed to process document")

if __name__ == "__main__":
    asyncio.run(main())
