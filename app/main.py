"""
SIT RAG Chatbot - FastAPI Application
Main application with CORS and startup events.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models import HealthResponse
from app.routers import chat

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting SIT RAG Chatbot...")
    settings = get_settings()
    logger.info(f"LLM Model: {settings.llm_model}")
    logger.info(f"Embedding Model: {settings.embedding_model}")
    
    # Initialize RAG service and load vectors
    try:
        rag_service = chat.get_rag_service()
        # Auto-ingest documents if vector store is empty
        if rag_service.vector_store.count() == 0:
            logger.info("Vector store empty, checking for documents...")
            result = rag_service.ingest_documents()
            logger.info(f"Ingestion result: {result}")
    except Exception as e:
        logger.warning(f"Could not initialize RAG service on startup: {e}")
        logger.warning("Make sure GOOGLE_API_KEY is set in .env file")
    
    yield
    
    # Shutdown
    logger.info("Shutting down SIT RAG Chatbot...")


# Create FastAPI application
app = FastAPI(
    title="SIT RAG Chatbot",
    description="""
    Official Academic Assistant for Siddaganga Institute of Technology (SIT), Tumakuru.
    
    This chatbot provides accurate information from official SIT documents and the sit.ac.in website.
    
    ## Features
    - **Strict Information Governance**: Answers only from official documents
    - **Zero Hallucination**: Refuses to answer if information is not available
    - **Multiple Query Modes**: Student, Exam, and Faculty modes
    - **Source Citations**: Every answer includes source references
    
    ## Usage
    1. POST to `/api/ask` with your question
    2. Optionally specify query mode (student, exam, faculty)
    3. Receive answer with source citations
    
    ## Important
    For the most accurate and up-to-date information, always verify with:
    - Official SIT Website: https://sit.ac.in
    - Relevant Department
    """,
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check."""
    return HealthResponse(
        status="healthy",
        service="SIT RAG Chatbot",
        version="1.0.0"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="SIT RAG Chatbot",
        version="1.0.0"
    )


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
