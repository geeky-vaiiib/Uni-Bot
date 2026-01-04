"""
SIT RAG Chatbot - RAG Retrieval Service
Uses Ollama for local LLM inference - no API limits!
"""

import logging
from typing import List, Dict, Any, Optional
import requests

from core.embeddings import EmbeddingService
from core.vectorstore import FAISSVectorStore
from core.ingestion import DocumentLoader, AcademicChunker

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = "http://localhost:11434"


class RAGService:
    """
    Complete RAG service using Ollama for local LLM.
    No API quotas or limits!
    """
    
    # System prompts for different modes
    SYSTEM_PROMPTS = {
        "student": """You are the official Academic Assistant for Siddaganga Institute of Technology (SIT), Tumakuru.

IMPORTANT RULES:
1. Only answer based on the provided context from official SIT documents
2. If information is not in the context, say "I don't have this information in my current knowledge base. Please contact the relevant SIT department."
3. Always be helpful and professional
4. Cite sources when possible

You are helping students with questions about admissions, academics, rules, and campus life.""",

        "exam": """You are the official Examination Assistant for Siddaganga Institute of Technology (SIT), Tumakuru.

IMPORTANT RULES:
1. Only answer based on the provided context from official SIT documents
2. If information is not in the context, say "I don't have this specific examination information. Please contact the Controller of Examinations office."
3. Be precise about dates, rules, and requirements
4. For urgent matters, always recommend contacting the examination office

You are helping with examination-related queries.""",

        "faculty": """You are the official Academic Information System for Siddaganga Institute of Technology (SIT), Tumakuru.

IMPORTANT RULES:
1. Only answer based on the provided context from official SIT documents
2. If information is not in the context, acknowledge the limitation
3. Provide detailed, professional responses
4. Reference specific regulations and policies when available

You are assisting faculty and staff with academic policy queries."""
    }
    
    def __init__(
        self,
        google_api_key: Optional[str] = None,  # Kept for compatibility
        embedding_model: str = "nomic-embed-text",
        llm_model: str = "llama3.2",
        llm_temperature: float = 0.1,
        vector_store_path: str = "./data/vectorstore",
        documents_path: str = "./data/documents",
        top_k: int = 5,
        chunk_size: int = 1000,
        chunk_overlap: int = 200
    ):
        """Initialize the RAG service with Ollama."""
        self.llm_model = llm_model
        self.llm_temperature = llm_temperature
        self.top_k = top_k
        
        # Initialize components
        self.embedding_service = EmbeddingService(
            model=embedding_model,
            cache_enabled=True
        )
        
        self.vector_store = FAISSVectorStore(
            dimension=self.embedding_service.dimension,
            store_path=vector_store_path
        )
        
        self.document_loader = DocumentLoader(documents_path)
        self.chunker = AcademicChunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        
        self.documents_path = documents_path
        
        logger.info(f"RAG service initialized with Ollama (LLM: {llm_model})")
    
    def _generate_response(self, prompt: str, system_prompt: str) -> str:
        """
        Generate response using Ollama.
        
        Args:
            prompt: The user prompt with context
            system_prompt: System prompt for the mode
            
        Returns:
            Generated response text
        """
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": self.llm_model,
                    "prompt": prompt,
                    "system": system_prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.llm_temperature
                    }
                },
                timeout=120
            )
            response.raise_for_status()
            result = response.json()
            return result["response"]
        except Exception as e:
            logger.error(f"Ollama generation failed: {e}")
            raise
    
    def ask(self, question: str, mode: str = "student") -> Dict[str, Any]:
        """
        Answer a question using RAG.
        
        Args:
            question: The user's question
            mode: Query mode (student, exam, faculty)
            
        Returns:
            Dict with answer, sources, and confidence
        """
        # Get system prompt for mode
        system_prompt = self.SYSTEM_PROMPTS.get(mode, self.SYSTEM_PROMPTS["student"])
        
        # Embed the question
        query_embedding = self.embedding_service.embed_query(question)
        
        # Search for relevant documents
        results = self.vector_store.search(query_embedding, top_k=self.top_k)
        
        if not results:
            return {
                "answer": "I don't have any information about this topic in my knowledge base. Please contact the relevant SIT department for assistance.",
                "sources": [],
                "confidence": "no_context"
            }
        
        # Build context from results
        context_parts = []
        sources = []
        
        for i, result in enumerate(results, 1):
            content = result.get("content", "")
            # Metadata is at top level in search results
            source = result.get("source", "Unknown")
            page = result.get("page")
            section = result.get("section")
            
            context_parts.append(f"[Source {i}]: {content}")
            sources.append({
                "content": content[:200] + "..." if len(content) > 200 else content,
                "source": source,
                "page": page,
                "section": section
            })
        
        context = "\n\n".join(context_parts)
        
        # Build prompt
        prompt = f"""Based on the following context from official SIT documents, please answer the question.

CONTEXT:
{context}

QUESTION: {question}

Please provide a helpful and accurate answer based only on the context provided. If the context doesn't contain enough information, say so."""
        
        # Generate response
        answer = self._generate_response(prompt, system_prompt)
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": "verified"
        }
    
    def ingest_documents(self, force_reload: bool = False) -> Dict[str, Any]:
        """
        Ingest documents into the vector store.
        
        Args:
            force_reload: If True, clear existing vectors and reload
            
        Returns:
            Status information about the ingestion
        """
        if force_reload:
            self.vector_store.clear()
            logger.info("Cleared existing vector store")
        
        # Load documents
        documents = self.document_loader.load_all()
        
        if not documents:
            logger.warning("No documents found to ingest")
            return {"status": "no_documents", "documents_found": 0}
        
        # Chunk documents
        all_chunks = []
        all_metadata = []
        
        for doc in documents:
            chunks = self.chunker.chunk_document(doc.content, doc.metadata)
            for chunk in chunks:
                all_chunks.append(chunk.content)
                all_metadata.append(chunk.metadata)
        
        logger.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        
        # Generate embeddings
        embeddings = self.embedding_service.embed_batch(all_chunks)
        
        # Add to vector store (embeddings, documents, metadatas)
        self.vector_store.add(embeddings, all_chunks, all_metadata)
        
        # Save vector store
        self.vector_store.save()
        
        return {
            "status": "success",
            "documents_processed": len(documents),
            "chunks_created": len(all_chunks),
            "vectors_stored": self.vector_store.count()
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the RAG service."""
        return {
            "vector_store": self.vector_store.get_stats(),
            "embedding_cache_size": self.embedding_service.get_cache_size(),
            "documents_path": self.documents_path,
            "document_count": self.document_loader.get_document_count(),
            "llm_model": self.llm_model
        }
