"""
SIT RAG Chatbot - Academic-Safe Chunker
Chunking logic that preserves section headings and academic document structure.
"""

import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    """Represents a document chunk with content and metadata."""
    content: str
    metadata: Dict[str, Any]
    chunk_id: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "content": self.content,
            "chunk_id": self.chunk_id,
            **self.metadata
        }


class AcademicChunker:
    """
    Academic-safe chunker that preserves document structure.
    - Keeps section headings with their content
    - Respects paragraph boundaries
    - Maintains context for regulations and rules
    """
    
    # Patterns for detecting section headings in academic documents
    HEADING_PATTERNS = [
        r"^#{1,6}\s+.+$",  # Markdown headings
        r"^\d+\.\s+[A-Z].*$",  # Numbered sections like "1. INTRODUCTION"
        r"^\d+\.\d+\s+.+$",  # Sub-sections like "1.1 Overview"
        r"^[A-Z][A-Z\s]{2,}:?\s*$",  # ALL CAPS headings
        r"^(?:CHAPTER|SECTION|ARTICLE|REGULATION)\s+\d+",  # Document divisions
        r"^[IVXLC]+\.\s+.+$",  # Roman numeral sections
    ]
    
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        preserve_headings: bool = True
    ):
        """
        Initialize the chunker.
        
        Args:
            chunk_size: Maximum size of each chunk in characters
            chunk_overlap: Overlap between consecutive chunks
            preserve_headings: Whether to preserve section headings
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.preserve_headings = preserve_headings
        
        # Compile heading patterns
        self.heading_regex = re.compile(
            "|".join(self.HEADING_PATTERNS),
            re.MULTILINE
        )
    
    def chunk_document(self, content: str, metadata: Dict[str, Any]) -> List[Chunk]:
        """
        Chunk a document while preserving structure.
        
        Args:
            content: Document text content
            metadata: Document metadata
        
        Returns:
            List of Chunk objects
        """
        if not content.strip():
            return []
        
        # First, split by sections if possible
        sections = self._split_by_sections(content)
        
        chunks = []
        chunk_id = 0
        
        for section in sections:
            section_heading = section.get("heading", "")
            section_content = section.get("content", "")
            
            # If section is small enough, keep it as one chunk
            if len(section_content) <= self.chunk_size:
                chunk_content = section_content
                if section_heading and self.preserve_headings:
                    chunk_content = f"{section_heading}\n\n{section_content}"
                
                if chunk_content.strip():
                    chunks.append(Chunk(
                        content=chunk_content.strip(),
                        metadata={
                            **metadata,
                            "section": section_heading,
                            "chunk_id": chunk_id
                        },
                        chunk_id=chunk_id
                    ))
                    chunk_id += 1
            else:
                # Split large sections while preserving context
                section_chunks = self._split_large_section(
                    section_content,
                    section_heading,
                    metadata,
                    chunk_id
                )
                chunks.extend(section_chunks)
                chunk_id += len(section_chunks)
        
        logger.info(f"Created {len(chunks)} chunks from document: {metadata.get('source', 'unknown')}")
        return chunks
    
    def _split_by_sections(self, content: str) -> List[Dict[str, str]]:
        """Split content by detected section headings."""
        lines = content.split("\n")
        sections = []
        current_heading = ""
        current_content = []
        
        for line in lines:
            # Check if this line is a heading
            if self.heading_regex.match(line.strip()):
                # Save previous section
                if current_content:
                    sections.append({
                        "heading": current_heading,
                        "content": "\n".join(current_content).strip()
                    })
                current_heading = line.strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Don't forget the last section
        if current_content:
            sections.append({
                "heading": current_heading,
                "content": "\n".join(current_content).strip()
            })
        
        # If no sections detected, treat entire content as one section
        if not sections:
            sections = [{"heading": "", "content": content.strip()}]
        
        return sections
    
    def _split_large_section(
        self,
        content: str,
        heading: str,
        metadata: Dict[str, Any],
        start_chunk_id: int
    ) -> List[Chunk]:
        """Split a large section into smaller chunks with overlap."""
        chunks = []
        
        # Split by paragraphs first
        paragraphs = re.split(r"\n\s*\n", content)
        
        current_chunk = ""
        chunk_id = start_chunk_id
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            # Check if adding this paragraph would exceed chunk size
            test_chunk = current_chunk + "\n\n" + para if current_chunk else para
            
            if len(test_chunk) > self.chunk_size and current_chunk:
                # Save current chunk
                chunk_content = current_chunk
                if heading and self.preserve_headings:
                    chunk_content = f"{heading}\n\n{current_chunk}"
                
                chunks.append(Chunk(
                    content=chunk_content.strip(),
                    metadata={
                        **metadata,
                        "section": heading,
                        "chunk_id": chunk_id
                    },
                    chunk_id=chunk_id
                ))
                chunk_id += 1
                
                # Start new chunk with overlap
                overlap_content = self._get_overlap_content(current_chunk)
                current_chunk = overlap_content + "\n\n" + para if overlap_content else para
            else:
                current_chunk = test_chunk
        
        # Don't forget the last chunk
        if current_chunk.strip():
            chunk_content = current_chunk
            if heading and self.preserve_headings:
                chunk_content = f"{heading}\n\n{current_chunk}"
            
            chunks.append(Chunk(
                content=chunk_content.strip(),
                metadata={
                    **metadata,
                    "section": heading,
                    "chunk_id": chunk_id
                },
                chunk_id=chunk_id
            ))
        
        return chunks
    
    def _get_overlap_content(self, content: str) -> str:
        """Get the overlap content from the end of a chunk."""
        if len(content) <= self.chunk_overlap:
            return content
        
        # Try to break at a sentence or paragraph boundary
        overlap_text = content[-self.chunk_overlap:]
        
        # Find a sentence boundary
        sentence_match = re.search(r"[.!?]\s+", overlap_text)
        if sentence_match:
            return overlap_text[sentence_match.end():]
        
        return overlap_text
    
    def chunk_all(self, documents: List[Any]) -> List[Chunk]:
        """
        Chunk multiple documents.
        
        Args:
            documents: List of Document objects
        
        Returns:
            List of all chunks
        """
        all_chunks = []
        
        for doc in documents:
            chunks = self.chunk_document(doc.content, doc.metadata)
            all_chunks.extend(chunks)
        
        logger.info(f"Total chunks created: {len(all_chunks)}")
        return all_chunks
