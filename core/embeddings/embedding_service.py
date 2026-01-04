"""
SIT RAG Chatbot - Embedding Service
Ollama-based local embedding service - no API limits!
"""

import hashlib
from typing import List, Optional, Dict
import logging
import requests

logger = logging.getLogger(__name__)

OLLAMA_BASE_URL = "http://localhost:11434"


class EmbeddingService:
    """
    Embedding service using Ollama's local embedding models.
    No API limits, runs entirely locally.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,  # Kept for compatibility, not used
        model: str = "nomic-embed-text",
        cache_enabled: bool = True
    ):
        """
        Initialize the embedding service.
        
        Args:
            api_key: Not used for Ollama, kept for compatibility
            model: Ollama embedding model to use
            cache_enabled: Whether to cache embeddings
        """
        self.model = model
        self.cache_enabled = cache_enabled
        self._cache: Dict[str, List[float]] = {}
        
        # nomic-embed-text has 768 dimensions
        self.dimension = 768
        
        # Verify Ollama is running
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            if response.status_code == 200:
                logger.info(f"Ollama embedding service initialized with model: {self.model}")
            else:
                logger.warning("Ollama may not be running properly")
        except Exception as e:
            logger.warning(f"Could not connect to Ollama: {e}")
            logger.warning("Make sure Ollama is running: brew services start ollama")
    
    def _embed(self, text: str) -> List[float]:
        """
        Generate embedding using Ollama API.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/embeddings",
                json={
                    "model": self.model,
                    "prompt": text
                },
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result["embedding"]
        except Exception as e:
            logger.error(f"Ollama embedding failed: {e}")
            raise
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
        
        Returns:
            Embedding vector as list of floats
        """
        if not text.strip():
            raise ValueError("Cannot embed empty text")
        
        # Check cache
        if self.cache_enabled:
            cache_key = self._get_cache_key(text)
            if cache_key in self._cache:
                logger.debug("Cache hit for embedding")
                return self._cache[cache_key]
        
        embedding = self._embed(text)
        
        # Cache the result
        if self.cache_enabled:
            self._cache[cache_key] = embedding
        
        return embedding
    
    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a query.
        
        Args:
            text: Query text to embed
        
        Returns:
            Embedding vector as list of floats
        """
        if not text.strip():
            raise ValueError("Cannot embed empty text")
        
        # Check cache
        if self.cache_enabled:
            cache_key = self._get_cache_key(f"query:{text}")
            if cache_key in self._cache:
                logger.debug("Cache hit for query embedding")
                return self._cache[cache_key]
        
        embedding = self._embed(text)
        
        # Cache the result
        if self.cache_enabled:
            self._cache[cache_key] = embedding
        
        return embedding
    
    def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            batch_size: Not used, kept for compatibility
        
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        all_embeddings = []
        
        for i, text in enumerate(texts):
            if not text.strip():
                all_embeddings.append([0.0] * self.dimension)
                continue
            
            try:
                embedding = self.embed_text(text)
                all_embeddings.append(embedding)
                
                if (i + 1) % 50 == 0:
                    logger.info(f"Embedded {i + 1}/{len(texts)} texts")
            except Exception as e:
                logger.error(f"Failed to embed text: {e}")
                all_embeddings.append([0.0] * self.dimension)
        
        logger.info(f"Embedded {len(texts)} texts")
        return all_embeddings
    
    def _get_cache_key(self, text: str) -> str:
        """Generate a cache key for the given text."""
        return hashlib.md5(f"{self.model}:{text}".encode()).hexdigest()
    
    def clear_cache(self):
        """Clear the embedding cache."""
        self._cache.clear()
        logger.info("Embedding cache cleared")
    
    def get_cache_size(self) -> int:
        """Get the number of cached embeddings."""
        return len(self._cache)
