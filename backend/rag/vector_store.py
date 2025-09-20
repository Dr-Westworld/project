"""
Vector Store and RAG Pipeline for Legal Document Assistant
Handles document chunking, embedding generation, and retrieval
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from dataclasses import dataclass
from datetime import datetime
import json
import hashlib
import re
from sentence_transformers import SentenceTransformer
import pinecone
from pinecone import Pinecone, ServerlessSpec
import openai
from google.cloud import aiplatform
from google.cloud.aiplatform.gapic.schema import predict
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class DocumentChunk:
    """Represents a chunk of a document with metadata"""
    id: str
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    source_url: Optional[str] = None
    page_number: Optional[int] = None
    chunk_index: Optional[int] = None

@dataclass
class SearchResult:
    """Represents a search result from vector store"""
    chunk: DocumentChunk
    similarity_score: float
    rank: int

class DocumentChunker:
    """Handles document chunking for optimal retrieval"""
    
    def __init__(self, chunk_size: int = 512, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[DocumentChunk]:
        """Split text into overlapping chunks"""
        if metadata is None:
            metadata = {}
        
        # Clean and normalize text
        text = self.clean_text(text)
        
        # Split into sentences first
        sentences = self.split_into_sentences(text)
        
        chunks = []
        current_chunk = ""
        chunk_index = 0
        
        for sentence in sentences:
            # If adding this sentence would exceed chunk size, save current chunk
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                chunk_id = self.generate_chunk_id(text, chunk_index)
                chunks.append(DocumentChunk(
                    id=chunk_id,
                    content=current_chunk.strip(),
                    metadata={**metadata, 'chunk_index': chunk_index},
                    chunk_index=chunk_index
                ))
                
                # Start new chunk with overlap
                overlap_text = self.get_overlap_text(current_chunk, self.overlap)
                current_chunk = overlap_text + " " + sentence
                chunk_index += 1
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add final chunk
        if current_chunk.strip():
            chunk_id = self.generate_chunk_id(text, chunk_index)
            chunks.append(DocumentChunk(
                id=chunk_id,
                content=current_chunk.strip(),
                metadata={**metadata, 'chunk_index': chunk_index},
                chunk_index=chunk_index
            ))
        
        return chunks
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
        
        return text.strip()
    
    def split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting (can be improved with NLTK or spaCy)
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def get_overlap_text(self, text: str, overlap_size: int) -> str:
        """Get the last part of text for overlap"""
        words = text.split()
        if len(words) <= overlap_size:
            return text
        return " ".join(words[-overlap_size:])
    
    def generate_chunk_id(self, text: str, chunk_index: int) -> str:
        """Generate unique chunk ID"""
        content_hash = hashlib.md5(text.encode()).hexdigest()[:8]
        return f"chunk_{content_hash}_{chunk_index}"

class EmbeddingGenerator:
    """Generates embeddings for text chunks"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the embedding model"""
        try:
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded embedding model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error loading embedding model: {str(e)}")
            raise
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text"""
        try:
            embedding = self.model.encode(text, convert_to_tensor=False)
            return embedding.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return []
    
    def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts"""
        try:
            embeddings = self.model.encode(texts, convert_to_tensor=False)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating batch embeddings: {str(e)}")
            return []

class VectorStore:
    """Vector store for document chunks and legal sources"""
    
    def __init__(self, pinecone_api_key: str, pinecone_environment: str = "us-west1-gcp"):
        self.pinecone_api_key = pinecone_api_key
        self.pinecone_environment = pinecone_environment
        self.pc = None
        self.index = None
        self.embedding_generator = EmbeddingGenerator()
        self._initialize_pinecone()
    
    def _initialize_pinecone(self):
        """Initialize Pinecone connection"""
        try:
            self.pc = Pinecone(api_key=self.pinecone_api_key)
            
            # Create or get index
            index_name = "legal-documents"
            if index_name not in self.pc.list_indexes().names():
                self.pc.create_index(
                    name=index_name,
                    dimension=384,  # Dimension for all-MiniLM-L6-v2
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region="us-east-1"
                    )
                )
            
            self.index = self.pc.Index(index_name)
            logger.info("Pinecone initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {str(e)}")
            raise
    
    def add_chunks(self, chunks: List[DocumentChunk]) -> bool:
        """Add document chunks to vector store"""
        try:
            # Generate embeddings for chunks
            texts = [chunk.content for chunk in chunks]
            embeddings = self.embedding_generator.generate_embeddings_batch(texts)
            
            # Prepare vectors for Pinecone
            vectors = []
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                if embedding:  # Only add if embedding was generated
                    vectors.append({
                        'id': chunk.id,
                        'values': embedding,
                        'metadata': {
                            'content': chunk.content,
                            'source_url': chunk.source_url,
                            'page_number': chunk.page_number,
                            'chunk_index': chunk.chunk_index,
                            **chunk.metadata
                        }
                    })
            
            # Upsert to Pinecone
            if vectors:
                self.index.upsert(vectors=vectors)
                logger.info(f"Added {len(vectors)} chunks to vector store")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error adding chunks to vector store: {str(e)}")
            return False
    
    def search(self, query: str, top_k: int = 5, filter_dict: Dict[str, Any] = None) -> List[SearchResult]:
        """Search for similar chunks"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_generator.generate_embedding(query)
            if not query_embedding:
                return []
            
            # Search in Pinecone
            search_response = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True,
                filter=filter_dict
            )
            
            # Convert to SearchResult objects
            results = []
            for i, match in enumerate(search_response.matches):
                chunk = DocumentChunk(
                    id=match.id,
                    content=match.metadata.get('content', ''),
                    metadata=match.metadata,
                    source_url=match.metadata.get('source_url'),
                    page_number=match.metadata.get('page_number'),
                    chunk_index=match.metadata.get('chunk_index')
                )
                
                results.append(SearchResult(
                    chunk=chunk,
                    similarity_score=match.score,
                    rank=i + 1
                ))
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching vector store: {str(e)}")
            return []
    
    def delete_chunks(self, chunk_ids: List[str]) -> bool:
        """Delete chunks from vector store"""
        try:
            self.index.delete(ids=chunk_ids)
            logger.info(f"Deleted {len(chunk_ids)} chunks from vector store")
            return True
        except Exception as e:
            logger.error(f"Error deleting chunks: {str(e)}")
            return False

class RAGPipeline:
    """Retrieval-Augmented Generation pipeline for legal documents"""
    
    def __init__(self, vector_store: VectorStore, openai_api_key: str):
        self.vector_store = vector_store
        self.openai_api_key = openai_api_key
        openai.api_key = openai_api_key
        self.chunker = DocumentChunker()
    
    def process_document(self, document_content: str, metadata: Dict[str, Any] = None) -> bool:
        """Process a document and add it to the vector store"""
        try:
            # Chunk the document
            chunks = self.chunker.chunk_text(document_content, metadata)
            
            # Add chunks to vector store
            success = self.vector_store.add_chunks(chunks)
            
            if success:
                logger.info(f"Processed document into {len(chunks)} chunks")
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            return False
    
    def retrieve_relevant_chunks(self, query: str, top_k: int = 5, 
                                jurisdiction: str = None, 
                                document_type: str = None) -> List[SearchResult]:
        """Retrieve relevant chunks for a query"""
        try:
            # Build filter for jurisdiction and document type
            filter_dict = {}
            if jurisdiction:
                filter_dict['jurisdiction'] = jurisdiction
            if document_type:
                filter_dict['document_type'] = document_type
            
            # Search vector store
            results = self.vector_store.search(query, top_k=top_k, filter_dict=filter_dict)
            
            # Filter by minimum similarity score
            min_score = 0.7
            filtered_results = [r for r in results if r.similarity_score >= min_score]
            
            return filtered_results
            
        except Exception as e:
            logger.error(f"Error retrieving chunks: {str(e)}")
            return []
    
    def generate_response(self, query: str, context_chunks: List[SearchResult], 
                         task_type: str = "general") -> str:
        """Generate response using retrieved context"""
        try:
            # Prepare context from chunks
            context_text = self.prepare_context(context_chunks)
            
            # Create prompt based on task type
            prompt = self.create_prompt(query, context_text, task_type)
            
            # Generate response using OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a legal assistant that helps users understand legal processes and documents. Provide accurate, helpful information based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I apologize, but I encountered an error while generating a response. Please try again."
    
    def prepare_context(self, chunks: List[SearchResult]) -> str:
        """Prepare context from retrieved chunks"""
        context_parts = []
        
        for i, result in enumerate(chunks, 1):
            chunk = result.chunk
            context_parts.append(f"Source {i} (Relevance: {result.similarity_score:.2f}):\n{chunk.content}\n")
        
        return "\n".join(context_parts)
    
    def create_prompt(self, query: str, context: str, task_type: str) -> str:
        """Create prompt for different task types"""
        base_prompt = f"""
Based on the following legal sources and context, please answer the user's question.

Context:
{context}

User Question: {query}

Please provide a comprehensive answer that:
1. Directly addresses the user's question
2. Cites specific sources when possible
3. Provides actionable steps if applicable
4. Mentions any important warnings or considerations
5. Suggests next steps or additional resources

Answer:
"""
        
        if task_type == "progress_path":
            base_prompt += "\n\nFormat your response as a structured progress path with clear steps, estimated timelines, and required documents."
        elif task_type == "document_analysis":
            base_prompt += "\n\nFocus on analyzing the specific document and explaining its key provisions and implications."
        elif task_type == "compliance":
            base_prompt += "\n\nEmphasize compliance requirements, deadlines, and regulatory considerations."
        
        return base_prompt
    
    def generate_progress_path(self, document_content: str, user_prompt: str, 
                              jurisdiction: str = None) -> Dict[str, Any]:
        """Generate a structured progress path from document and prompt"""
        try:
            # Process the document first
            metadata = {
                'jurisdiction': jurisdiction,
                'document_type': 'legal_document',
                'processed_at': datetime.now().isoformat()
            }
            
            self.process_document(document_content, metadata)
            
            # Retrieve relevant chunks for progress path generation
            progress_query = f"step by step process for {user_prompt}"
            relevant_chunks = self.retrieve_relevant_chunks(
                progress_query, 
                top_k=10,
                jurisdiction=jurisdiction
            )
            
            # Generate progress path
            context_text = self.prepare_context(relevant_chunks)
            prompt = f"""
Based on the following legal information, create a detailed step-by-step progress path for: {user_prompt}

Context:
{context_text}

Please create a structured progress path with:
1. Clear stage titles and descriptions
2. Required documents for each stage
3. Estimated timelines
4. Responsible parties
5. Dependencies between stages
6. Important warnings or considerations
7. Relevant website links and citations

Format as JSON with the following structure:
{{
    "taskTitle": "Brief title of the task",
    "description": "Detailed description",
    "jurisdiction": "{jurisdiction or 'Unknown'}",
    "stages": [
        {{
            "id": "stage_1",
            "title": "Stage title",
            "shortDescription": "Brief description",
            "description": "Detailed description",
            "estimatedTime": "X hours/days",
            "requiredDocuments": ["Document 1", "Document 2"],
            "responsibleParty": "user/lawyer/third_party",
            "dependencies": ["stage_id"],
            "confidence": "high/medium/low",
            "citations": [
                {{
                    "url": "source_url",
                    "title": "Source title",
                    "source_type": "government/court/portal",
                    "excerpt": "Relevant excerpt"
                }}
            ],
            "warnings": ["Important warning"],
            "subStages": [
                {{
                    "id": "stage_1_1",
                    "title": "Sub-stage title",
                    "shortDescription": "Brief description",
                    "estimatedTime": "X minutes/hours",
                    "requiredDocuments": ["Document"],
                    "responsibleParty": "user"
                }}
            ]
        }}
    ]
}}
"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a legal expert that creates detailed, accurate progress paths for legal processes. Always provide structured, actionable information."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            # Parse JSON response
            response_text = response.choices[0].message.content.strip()
            
            # Extract JSON from response (in case there's extra text)
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_text = response_text[json_start:json_end]
                progress_data = json.loads(json_text)
                return progress_data
            
            # Fallback if JSON parsing fails
            return {
                "taskTitle": f"Progress Path for {user_prompt}",
                "description": response_text,
                "jurisdiction": jurisdiction or "Unknown",
                "stages": []
            }
            
        except Exception as e:
            logger.error(f"Error generating progress path: {str(e)}")
            return {
                "taskTitle": f"Progress Path for {user_prompt}",
                "description": "Error generating progress path. Please try again.",
                "jurisdiction": jurisdiction or "Unknown",
                "stages": []
            }

# Example usage
async def main():
    """Example usage of the RAG pipeline"""
    # Initialize components
    vector_store = VectorStore(
        pinecone_api_key="your-pinecone-api-key",
        pinecone_environment="us-west1-gcp"
    )
    
    rag_pipeline = RAGPipeline(
        vector_store=vector_store,
        openai_api_key="your-openai-api-key"
    )
    
    # Example document
    document_content = """
    To register an LLC in California, you must:
    1. Choose a unique name for your LLC
    2. File Articles of Organization with the Secretary of State
    3. Pay the required filing fee
    4. Obtain necessary business licenses
    """
    
    # Generate progress path
    progress_path = rag_pipeline.generate_progress_path(
        document_content=document_content,
        user_prompt="register LLC in California",
        jurisdiction="California, USA"
    )
    
    print(json.dumps(progress_path, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
