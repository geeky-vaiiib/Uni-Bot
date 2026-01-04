"""
SIT RAG Chatbot - FAISS Vector Store
FAISS-based vector store with metadata support and top-k retrieval.
"""

import os
import json
import pickle
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import logging

import numpy as np

try:
    import faiss
except ImportError:
    faiss = None

logger = logging.getLogger(__name__)


class FAISSVectorStore:
    """
    FAISS-based vector store for the SIT RAG pipeline.
    Supports metadata storage and persistence.
    """
    
    def __init__(
        self,
        dimension: int = 1536,
        store_path: Optional[str] = None
    ):
        """
        Initialize the FAISS vector store.
        
        Args:
            dimension: Embedding dimension
            store_path: Path to persist the index
        """
        if faiss is None:
            raise ImportError("FAISS is not installed. Run: pip install faiss-cpu")
        
        self.dimension = dimension
        self.store_path = Path(store_path) if store_path else None
        
        # Initialize FAISS index (L2 distance)
        self.index = faiss.IndexFlatL2(dimension)
        
        # Metadata storage (maps index position to metadata)
        self.metadata: List[Dict[str, Any]] = []
        self.documents: List[str] = []  # Store original text
        
        # Load existing index if available
        if self.store_path and self.store_path.exists():
            self.load()
        
        logger.info(f"FAISS vector store initialized with dimension {dimension}")
    
    def add(
        self,
        embeddings: List[List[float]],
        documents: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None
    ) -> None:
        """
        Add documents with their embeddings to the store.
        
        Args:
            embeddings: List of embedding vectors
            documents: List of document texts
            metadatas: Optional list of metadata dicts
        """
        if not embeddings:
            logger.warning("No embeddings to add")
            return
        
        if len(embeddings) != len(documents):
            raise ValueError("Embeddings and documents must have same length")
        
        if metadatas and len(metadatas) != len(documents):
            raise ValueError("Metadatas must have same length as documents")
        
        # Convert to numpy array
        vectors = np.array(embeddings, dtype=np.float32)
        
        # Add to FAISS index
        self.index.add(vectors)
        
        # Store documents and metadata
        self.documents.extend(documents)
        
        if metadatas:
            self.metadata.extend(metadatas)
        else:
            self.metadata.extend([{} for _ in documents])
        
        logger.info(f"Added {len(embeddings)} vectors to the store")
    
    def search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        threshold: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar documents.
        
        Args:
            query_embedding: Query embedding vector
            top_k: Number of results to return
            threshold: Optional distance threshold for filtering
        
        Returns:
            List of results with content, metadata, and distance
        """
        if self.index.ntotal == 0:
            logger.warning("Vector store is empty")
            return []
        
        # Convert query to numpy array
        query_vector = np.array([query_embedding], dtype=np.float32)
        
        # Search
        distances, indices = self.index.search(query_vector, min(top_k, self.index.ntotal))
        
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx == -1:  # No result
                continue
            
            if threshold is not None and distance > threshold:
                continue
            
            result = {
                "content": self.documents[idx],
                "distance": float(distance),
                "score": 1 / (1 + float(distance)),  # Convert distance to similarity score
                **self.metadata[idx]
            }
            results.append(result)
        
        return results
    
    def save(self) -> None:
        """Persist the index and metadata to disk."""
        if not self.store_path:
            logger.warning("No store path configured, skipping save")
            return
        
        # Create directory if needed
        self.store_path.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_path = self.store_path / "index.faiss"
        faiss.write_index(self.index, str(index_path))
        
        # Save metadata and documents
        metadata_path = self.store_path / "metadata.pkl"
        with open(metadata_path, "wb") as f:
            pickle.dump({
                "metadata": self.metadata,
                "documents": self.documents,
                "dimension": self.dimension
            }, f)
        
        logger.info(f"Saved vector store to {self.store_path}")
    
    def load(self) -> bool:
        """Load index and metadata from disk."""
        if not self.store_path:
            return False
        
        index_path = self.store_path / "index.faiss"
        metadata_path = self.store_path / "metadata.pkl"
        
        if not index_path.exists() or not metadata_path.exists():
            logger.info("No existing index found, starting fresh")
            return False
        
        try:
            # Load FAISS index
            self.index = faiss.read_index(str(index_path))
            
            # Load metadata
            with open(metadata_path, "rb") as f:
                data = pickle.load(f)
                self.metadata = data["metadata"]
                self.documents = data["documents"]
                self.dimension = data.get("dimension", self.dimension)
            
            logger.info(f"Loaded vector store with {self.index.ntotal} vectors")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            return False
    
    def clear(self) -> None:
        """Clear the vector store."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.metadata = []
        self.documents = []
        
        if self.store_path:
            # Remove persisted files
            index_path = self.store_path / "index.faiss"
            metadata_path = self.store_path / "metadata.pkl"
            if index_path.exists():
                os.remove(index_path)
            if metadata_path.exists():
                os.remove(metadata_path)
        
        logger.info("Vector store cleared")
    
    def count(self) -> int:
        """Get the number of vectors in the store."""
        return self.index.ntotal
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store."""
        return {
            "total_vectors": self.index.ntotal,
            "dimension": self.dimension,
            "store_path": str(self.store_path) if self.store_path else None,
            "metadata_count": len(self.metadata),
            "documents_count": len(self.documents)
        }
