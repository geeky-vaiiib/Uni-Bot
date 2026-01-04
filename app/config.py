"""
SIT RAG Chatbot - Configuration
Environment-based settings using Pydantic Settings.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    
    # Google Gemini Configuration
    google_api_key: str
    embedding_model: str = "models/embedding-001"
    llm_model: str = "gemini-2.0-flash"
    llm_temperature: float = 0.1
    
    # RAG Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    top_k_results: int = 5
    
    # Vector Store
    vector_store_path: str = "./data/vectorstore"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Document Path
    documents_path: str = "./data/documents"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
