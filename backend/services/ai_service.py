"""
AI Service Integration
Combines document processing, web crawling, vector search, and LLM generation
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import os
from pathlib import Path

# Import our custom modules
from ..crawler.legal_crawler import LegalCrawler, LegalSource
from ..rag.vector_store import RAGPipeline, VectorStore, DocumentChunker
from ..document_processor import DocumentProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIService:
    """Main AI service that orchestrates all components"""
    
    def __init__(self, 
                 pinecone_api_key: str,
                 gemini_api_key: str,
                 google_cloud_project: str = None,
                 google_credentials_path: str = None):
        """
        Initialize AI service with all required API keys
        
        Args:
            pinecone_api_key: Pinecone API key for vector storage
            gemini_api_key: Google Gemini API key for LLM generation
            google_cloud_project: Google Cloud project ID
            google_credentials_path: Path to Google Cloud credentials JSON
        """
        self.pinecone_api_key = pinecone_api_key
        self.gemini_api_key = gemini_api_key
        self.google_cloud_project = google_cloud_project
        self.google_credentials_path = google_credentials_path
        
        # Initialize components
        self.vector_store = None
        self.rag_pipeline = None
        self.document_processor = None
        self.legal_crawler = None
        
        # Initialize services
        self._initialize_services()
    
    def _initialize_services(self):
        """Initialize all AI services"""
        try:
            # Initialize vector store
            self.vector_store = VectorStore(
                pinecone_api_key=self.pinecone_api_key,
                pinecone_environment="us-west1-gcp"
            )
            
            # Initialize RAG pipeline
            self.rag_pipeline = RAGPipeline(
                vector_store=self.vector_store,
                gemini_api_key=self.gemini_api_key
            )
            
            # Initialize document processor
            self.document_processor = DocumentProcessor(
                google_cloud_project=self.google_cloud_project,
                credentials_path=self.google_credentials_path
            )
            
            logger.info("AI services initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing AI services: {str(e)}")
            raise
    
    async def process_document(self, file_path: str, user_prompt: str, 
                              jurisdiction: str = None) -> Dict[str, Any]:
        """
        Process a legal document and generate a progress path
        
        Args:
            file_path: Path to the uploaded document
            user_prompt: User's description of what they need help with
            jurisdiction: Legal jurisdiction (e.g., "California, USA")
            
        Returns:
            Dictionary containing the generated progress path
        """
        try:
            logger.info(f"Processing document: {file_path}")
            
            # Step 1: Process document with Document AI
            document_data = await self.document_processor.process_document(file_path)
            
            if not document_data:
                raise Exception("Failed to process document")
            
            # Step 2: Crawl relevant legal sources
            legal_sources = await self._crawl_legal_sources(jurisdiction)
            
            # Step 3: Add legal sources to vector store
            await self._index_legal_sources(legal_sources)
            
            # Step 4: Generate progress path using RAG
            progress_path = await self._generate_progress_path(
                document_data, user_prompt, jurisdiction
            )
            
            # Step 5: Enhance progress path with web-crawled data
            enhanced_path = await self._enhance_progress_path(
                progress_path, legal_sources, jurisdiction
            )
            
            logger.info("Document processing completed successfully")
            return enhanced_path
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            return {
                "error": str(e),
                "taskTitle": f"Error processing {user_prompt}",
                "description": "An error occurred while processing your document. Please try again.",
                "stages": []
            }
    
    async def _crawl_legal_sources(self, jurisdiction: str = None) -> List[LegalSource]:
        """Crawl legal sources for the given jurisdiction"""
        try:
            async with LegalCrawler() as crawler:
                # Determine jurisdictions to crawl
                jurisdictions = [jurisdiction] if jurisdiction else ['California', 'New York', 'Texas', 'Federal']
                
                # Crawl legal sources
                sources = await crawler.crawl_legal_sources(jurisdictions)
                
                logger.info(f"Crawled {len(sources)} legal sources")
                return sources
                
        except Exception as e:
            logger.error(f"Error crawling legal sources: {str(e)}")
            return []
    
    async def _index_legal_sources(self, sources: List[LegalSource]):
        """Index legal sources in the vector store"""
        try:
            for source in sources:
                # Process each source as a document
                metadata = {
                    'source_type': source.source_type,
                    'jurisdiction': source.jurisdiction,
                    'authority_level': source.authority_level,
                    'url': source.url,
                    'title': source.title,
                    'last_crawled': source.last_crawled.isoformat()
                }
                
                # Add to vector store
                self.rag_pipeline.process_document(
                    document_content=source.content,
                    metadata=metadata
                )
            
            logger.info(f"Indexed {len(sources)} legal sources")
            
        except Exception as e:
            logger.error(f"Error indexing legal sources: {str(e)}")
    
    async def _generate_progress_path(self, document_data: Dict[str, Any], 
                                    user_prompt: str, jurisdiction: str) -> Dict[str, Any]:
        """Generate progress path using RAG pipeline"""
        try:
            # Extract text content from document
            document_text = document_data.get('text', '')
            
            # Generate progress path
            progress_path = self.rag_pipeline.generate_progress_path(
                document_content=document_text,
                user_prompt=user_prompt,
                jurisdiction=jurisdiction
            )
            
            return progress_path
            
        except Exception as e:
            logger.error(f"Error generating progress path: {str(e)}")
            return {
                "taskTitle": f"Progress Path for {user_prompt}",
                "description": "Error generating progress path",
                "stages": []
            }
    
    async def _enhance_progress_path(self, progress_path: Dict[str, Any], 
                                   legal_sources: List[LegalSource], 
                                   jurisdiction: str) -> Dict[str, Any]:
        """Enhance progress path with additional legal sources"""
        try:
            # Add metadata
            progress_path['metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'jurisdiction': jurisdiction,
                'sources_count': len(legal_sources),
                'enhanced_with_crawled_data': True
            }
            
            # Enhance each stage with additional sources
            for stage in progress_path.get('stages', []):
                stage_id = stage.get('id', '')
                
                # Search for relevant sources for this stage
                relevant_sources = await self._find_relevant_sources(
                    stage.get('title', '') + ' ' + stage.get('description', ''),
                    legal_sources
                )
                
                # Add citations to stage
                if 'citations' not in stage:
                    stage['citations'] = []
                
                for source in relevant_sources[:3]:  # Add top 3 relevant sources
                    stage['citations'].append({
                        'url': source.url,
                        'title': source.title,
                        'source_type': source.source_type,
                        'excerpt': source.content[:200] + '...' if len(source.content) > 200 else source.content,
                        'authority_level': source.authority_level
                    })
            
            return progress_path
            
        except Exception as e:
            logger.error(f"Error enhancing progress path: {str(e)}")
            return progress_path
    
    async def _find_relevant_sources(self, query: str, 
                                   sources: List[LegalSource]) -> List[LegalSource]:
        """Find relevant legal sources for a query"""
        try:
            # Use vector search to find relevant sources
            search_results = self.rag_pipeline.retrieve_relevant_chunks(
                query=query,
                top_k=5
            )
            
            # Map back to legal sources
            relevant_sources = []
            for result in search_results:
                source_url = result.chunk.metadata.get('url')
                if source_url:
                    # Find the corresponding legal source
                    for source in sources:
                        if source.url == source_url:
                            relevant_sources.append(source)
                            break
            
            return relevant_sources
            
        except Exception as e:
            logger.error(f"Error finding relevant sources: {str(e)}")
            return []
    
    async def expand_stage(self, stage_id: str, stage_context: str, 
                          jurisdiction: str = None) -> Dict[str, Any]:
        """Expand a stage with detailed sub-stages"""
        try:
            # Search for relevant information
            relevant_chunks = self.rag_pipeline.retrieve_relevant_chunks(
                query=stage_context,
                top_k=5,
                jurisdiction=jurisdiction
            )
            
            # Generate detailed sub-stages
            context_text = self.rag_pipeline.prepare_context(relevant_chunks)
            
            prompt = f"""
            Based on the following legal context, create detailed sub-stages for: {stage_context}
            
            Context:
            {context_text}
            
            Create 3-5 detailed sub-stages with:
            - Specific step-by-step instructions
            - Required documents
            - Estimated time
            - Website links if applicable
            - Warnings or important notes
            
            Format as JSON with subStages array.
            """
            
            # Generate response using Google Gemini
            from .gemini_client import generate_text

            system_msg = "You are a legal expert that creates detailed, actionable sub-steps for legal processes."
            full_prompt = system_msg + "\n\n" + prompt

            response_text = generate_text(
                prompt=full_prompt,
                model="gemini-pro",
                api_key=self.gemini_api_key,
                max_tokens=1000,
                temperature=0.3
            )
            
            # Try to parse JSON response
            try:
                json_start = response_text.find('[')
                json_end = response_text.rfind(']') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_text = response_text[json_start:json_end]
                    sub_stages = json.loads(json_text)
                    
                    return {
                        'id': stage_id,
                        'title': stage_context,
                        'subStages': sub_stages,
                        'enhanced_at': datetime.now().isoformat()
                    }
            except json.JSONDecodeError:
                pass
            
            # Fallback response
            return {
                'id': stage_id,
                'title': stage_context,
                'subStages': [
                    {
                        'id': f"{stage_id}_1",
                        'title': "Detailed Step 1",
                        'shortDescription': response_text[:100] + "...",
                        'estimatedTime': "30 minutes",
                        'responsibleParty': "user"
                    }
                ],
                'enhanced_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error expanding stage: {str(e)}")
            return {
                'id': stage_id,
                'title': stage_context,
                'subStages': [],
                'error': str(e)
            }
    
    async def chat_response(self, plan_id: str, message: str, 
                          context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate chat response about a progress plan"""
        try:
            # Retrieve relevant chunks for the chat message
            relevant_chunks = self.rag_pipeline.retrieve_relevant_chunks(
                query=message,
                top_k=5
            )
            
            # Generate response
            response = self.rag_pipeline.generate_response(
                query=message,
                context_chunks=relevant_chunks,
                task_type="general"
            )
            
            # Generate suggestions
            suggestions = [
                "What documents do I need for the next stage?",
                "How long will this process take?",
                "What are the common issues I should watch out for?",
                "Can you explain this stage in more detail?"
            ]
            
            return {
                'messageId': f"msg_{datetime.now().timestamp()}",
                'response': response,
                'suggestions': suggestions,
                'relatedStages': [chunk.metadata.get('stage_id') for chunk in relevant_chunks if chunk.metadata.get('stage_id')]
            }
            
        except Exception as e:
            logger.error(f"Error generating chat response: {str(e)}")
            return {
                'messageId': f"msg_{datetime.now().timestamp()}",
                'response': "I apologize, but I encountered an error while processing your message. Please try again.",
                'suggestions': [],
                'relatedStages': []
            }
    
    async def revalidate_plan(self, plan_id: str, additional_context: str = None) -> Dict[str, Any]:
        """Revalidate a plan with updated information"""
        try:
            # Re-crawl legal sources
            legal_sources = await self._crawl_legal_sources()
            
            # Re-index sources
            await self._index_legal_sources(legal_sources)
            
            # Generate updated plan
            # This would typically involve re-processing the original document
            # with the updated legal sources
            
            return {
                'planId': plan_id,
                'status': 'revalidated',
                'updatedAt': datetime.now().isoformat(),
                'sources_updated': len(legal_sources)
            }
            
        except Exception as e:
            logger.error(f"Error revalidating plan: {str(e)}")
            return {
                'planId': plan_id,
                'status': 'error',
                'error': str(e)
            }

# Factory function for easy initialization
def create_ai_service() -> AIService:
    """Create AI service with environment variables"""
    return AIService(
        pinecone_api_key=os.getenv('PINECONE_API_KEY'),
        gemini_api_key=os.getenv('GOOGLE_GEMINI_API_KEY'),
        google_cloud_project=os.getenv('GOOGLE_CLOUD_PROJECT_ID'),
        google_credentials_path=os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    )

# Example usage
async def main():
    """Example usage of the AI service"""
    # Initialize AI service
    ai_service = create_ai_service()
    
    # Process a document
    result = await ai_service.process_document(
        file_path="sample_contract.pdf",
        user_prompt="I need to understand this contract and what I need to do",
        jurisdiction="California, USA"
    )
    
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
