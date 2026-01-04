"""
SIT RAG Chatbot - API Models
Pydantic models for request/response validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class QueryMode(str, Enum):
    """Query mode for different user types."""
    STUDENT = "student"
    EXAM = "exam"
    FACULTY = "faculty"


class AskRequest(BaseModel):
    """Request model for /ask endpoint."""
    question: str = Field(
        ...,
        min_length=3,
        max_length=1000,
        description="The question to ask about SIT"
    )
    mode: QueryMode = Field(
        default=QueryMode.STUDENT,
        description="Query mode: student, exam, or faculty"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the minimum attendance requirement at SIT?",
                "mode": "student"
            }
        }


class SourceDocument(BaseModel):
    """Source document reference."""
    content: str = Field(..., description="Relevant content excerpt")
    source: str = Field(..., description="Source document name")
    page: Optional[int] = Field(None, description="Page number if applicable")
    section: Optional[str] = Field(None, description="Section heading if available")


class AskResponse(BaseModel):
    """Response model for /ask endpoint."""
    answer: str = Field(..., description="Generated answer from SIT documents")
    sources: List[SourceDocument] = Field(
        default=[],
        description="Source documents used to generate the answer"
    )
    query_mode: QueryMode = Field(..., description="Query mode used")
    confidence: str = Field(
        default="verified",
        description="Confidence level: verified, partial, or not_found"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "According to SIT Academic Regulations, the minimum attendance requirement is 75% in each subject.",
                "sources": [
                    {
                        "content": "A student shall have a minimum of 75% attendance...",
                        "source": "SIT_Academic_Regulations.pdf",
                        "page": 12,
                        "section": "Attendance Requirements"
                    }
                ],
                "query_mode": "student",
                "confidence": "verified"
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    service: str = "SIT RAG Chatbot"
    version: str = "1.0.0"
