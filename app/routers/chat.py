"""
SIT RAG Chatbot - Chat Router
POST /ask endpoint implementation.
"""

from fastapi import APIRouter, HTTPException, Depends
import logging

from app.models import AskRequest, AskResponse, SourceDocument
from app.config import get_settings, Settings
from core.rag import RAGService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["chat"])

# Global RAG service instance
_rag_service: RAGService = None


def get_rag_service() -> RAGService:
    """Get or create RAG service instance."""
    global _rag_service
    
    if _rag_service is None:
        settings = get_settings()
        _rag_service = RAGService(
            google_api_key=settings.google_api_key,
            embedding_model=settings.embedding_model,
            llm_model=settings.llm_model,
            llm_temperature=settings.llm_temperature,
            vector_store_path=settings.vector_store_path,
            documents_path=settings.documents_path,
            top_k=settings.top_k_results,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )
    
    return _rag_service


@router.post("/ask", response_model=AskResponse)
async def ask_question(
    request: AskRequest,
    rag_service: RAGService = Depends(get_rag_service)
) -> AskResponse:
    """
    Ask a question about SIT.
    
    This endpoint uses RAG to retrieve relevant information from official
    SIT documents and generate an accurate response.
    
    - **question**: The question about SIT (e.g., "What is the attendance requirement?")
    - **mode**: Query mode - `student`, `exam`, or `faculty`
    
    Returns the answer along with source documents used.
    """
    try:
        # Process the question
        result = rag_service.ask(
            question=request.question,
            mode=request.mode.value
        )
        
        # Convert sources to SourceDocument objects
        sources = [
            SourceDocument(
                content=src.get("content", ""),
                source=src.get("source", "Unknown"),
                page=src.get("page"),
                section=src.get("section")
            )
            for src in result.get("sources", [])
        ]
        
        return AskResponse(
            answer=result["answer"],
            sources=sources,
            query_mode=request.mode,
            confidence=result.get("confidence", "verified")
        )
        
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your question. Please try again."
        )


@router.post("/ingest")
async def ingest_documents(
    force_reload: bool = False,
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Ingest documents into the vector store.
    
    - **force_reload**: If true, clears existing index and reloads all documents
    
    This endpoint should be called after adding new documents to the data/documents folder.
    """
    try:
        result = rag_service.ingest_documents(force_reload=force_reload)
        return result
    except Exception as e:
        logger.error(f"Error ingesting documents: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to ingest documents: {str(e)}"
        )


@router.get("/status")
async def get_status(
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Get the status of the RAG service.
    
    Returns information about the vector store, document count, and system health.
    """
    try:
        return rag_service.get_status()
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to get service status"
        )
