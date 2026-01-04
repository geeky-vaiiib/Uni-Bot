"""
SIT RAG Chatbot - Document Loader
PDF and text file loading with metadata extraction for SIT documents.
Supports both text-based and scanned (image-based) PDFs via OCR.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

# PDF libraries
try:
    import fitz  # pymupdf
    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False

# OCR libraries
try:
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
    HAS_OCR = True
except ImportError:
    HAS_OCR = False

logger = logging.getLogger(__name__)


@dataclass
class Document:
    """Represents a loaded document with content and metadata."""
    content: str
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        if not self.metadata.get("source"):
            self.metadata["source"] = "Unknown"


class DocumentLoader:
    """
    Loads documents from PDF and text files for the SIT RAG pipeline.
    Supports PDF (text-based and scanned via OCR), TXT, and MD files.
    """
    
    SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}
    
    def __init__(self, documents_path: str):
        """
        Initialize the document loader.
        
        Args:
            documents_path: Path to the directory containing documents
        """
        self.documents_path = Path(documents_path)
        if not self.documents_path.exists():
            self.documents_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created documents directory: {self.documents_path}")
        
        # Log available libraries
        if HAS_FITZ:
            logger.info("PDF support: pymupdf (fitz)")
        if HAS_PDFPLUMBER:
            logger.info("PDF support: pdfplumber")
        if HAS_OCR:
            logger.info("OCR support: pytesseract + pdf2image")
        else:
            logger.warning("OCR not available (install pytesseract, pdf2image)")
    
    def load_all(self) -> List[Document]:
        """
        Load all supported documents from the documents directory.
        
        Returns:
            List of Document objects
        """
        documents = []
        
        for file_path in self.documents_path.rglob("*"):
            if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                try:
                    doc = self.load_file(file_path)
                    if doc and doc.content.strip():
                        documents.append(doc)
                        logger.info(f"Loaded: {file_path.name} ({len(doc.content)} chars)")
                except Exception as e:
                    logger.error(f"Failed to load {file_path}: {e}")
        
        logger.info(f"Total documents loaded: {len(documents)}")
        return documents
    
    def load_file(self, file_path: Path) -> Optional[Document]:
        """
        Load a single file.
        
        Args:
            file_path: Path to the file
        
        Returns:
            Document object or None if loading fails
        """
        extension = file_path.suffix.lower()
        
        if extension == ".pdf":
            return self._load_pdf(file_path)
        elif extension in {".txt", ".md"}:
            return self._load_text(file_path)
        else:
            logger.warning(f"Unsupported file type: {extension}")
            return None
    
    def _load_pdf(self, file_path: Path) -> Optional[Document]:
        """Load a PDF file, using OCR if needed for scanned documents."""
        
        # First try pdfplumber to check if it's text-based or scanned
        if HAS_PDFPLUMBER:
            doc = self._load_pdf_pdfplumber(file_path)
            if doc and len(doc.content.strip()) > 100:
                return doc
            else:
                logger.info(f"Little text found, trying OCR for {file_path.name}")
        
        # If no text found, try OCR
        if HAS_OCR:
            return self._load_pdf_ocr(file_path)
        
        # Fallback to fitz
        if HAS_FITZ:
            return self._load_pdf_fitz(file_path)
        
        logger.error("No PDF library available")
        return None
    
    def _load_pdf_pdfplumber(self, file_path: Path) -> Optional[Document]:
        """Load PDF using pdfplumber."""
        try:
            pages_content = []
            with pdfplumber.open(str(file_path)) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if text and text.strip():
                        pages_content.append({
                            "page": page_num,
                            "content": text.strip()
                        })
            
            full_content = "\n\n".join([p["content"] for p in pages_content])
            
            metadata = {
                "source": file_path.name,
                "file_path": str(file_path),
                "file_type": "pdf",
                "total_pages": len(pages_content),
                "extraction_method": "pdfplumber"
            }
            
            return Document(content=full_content, metadata=metadata)
            
        except Exception as e:
            logger.error(f"pdfplumber error for {file_path}: {e}")
            return None
    
    def _load_pdf_ocr(self, file_path: Path) -> Optional[Document]:
        """Load scanned PDF using OCR (Tesseract)."""
        try:
            logger.info(f"Starting OCR for {file_path.name}...")
            
            # Convert PDF to images
            images = convert_from_path(str(file_path), dpi=200)
            logger.info(f"Converted to {len(images)} images, running OCR...")
            
            pages_content = []
            for page_num, image in enumerate(images, 1):
                # Run OCR on image
                text = pytesseract.image_to_string(image, lang='eng')
                if text and text.strip():
                    pages_content.append({
                        "page": page_num,
                        "content": text.strip()
                    })
                
                # Log progress every 10 pages
                if page_num % 10 == 0:
                    logger.info(f"OCR progress: {page_num}/{len(images)} pages")
            
            full_content = "\n\n".join([p["content"] for p in pages_content])
            
            logger.info(f"OCR complete: {len(full_content)} chars extracted from {len(pages_content)} pages")
            
            metadata = {
                "source": file_path.name,
                "file_path": str(file_path),
                "file_type": "pdf",
                "total_pages": len(images),
                "pages_with_text": len(pages_content),
                "extraction_method": "ocr"
            }
            
            return Document(content=full_content, metadata=metadata)
            
        except Exception as e:
            logger.error(f"OCR error for {file_path}: {e}")
            return None
    
    def _load_pdf_fitz(self, file_path: Path) -> Optional[Document]:
        """Load PDF using pymupdf (fitz)."""
        try:
            doc = fitz.open(str(file_path))
            
            pages_content = []
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text("text")
                if text and text.strip():
                    pages_content.append({
                        "page": page_num + 1,
                        "content": text.strip()
                    })
            
            doc.close()
            
            full_content = "\n\n".join([p["content"] for p in pages_content])
            
            metadata = {
                "source": file_path.name,
                "file_path": str(file_path),
                "file_type": "pdf",
                "total_pages": len(pages_content),
                "extraction_method": "fitz"
            }
            
            return Document(content=full_content, metadata=metadata)
            
        except Exception as e:
            logger.error(f"fitz error for {file_path}: {e}")
            return None
    
    def _load_text(self, file_path: Path) -> Optional[Document]:
        """Load a text or markdown file."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            metadata = {
                "source": file_path.name,
                "file_path": str(file_path),
                "file_type": file_path.suffix.lower().replace(".", "")
            }
            
            return Document(content=content, metadata=metadata)
            
        except Exception as e:
            logger.error(f"Error loading text file {file_path}: {e}")
            return None
    
    def get_document_count(self) -> int:
        """Get count of supported documents in the directory."""
        count = 0
        for file_path in self.documents_path.rglob("*"):
            if file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                count += 1
        return count
