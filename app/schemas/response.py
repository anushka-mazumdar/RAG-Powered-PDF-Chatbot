"""
Pydantic response schemas
"""
from pydantic import BaseModel
from typing import List, Optional


class SuccessResponse(BaseModel):
    """Standard success response"""
    message: str
    data: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation successful",
                "data": {}
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "Internal server error",
                "detail": "An unexpected error occurred"
            }
        }


class AnswerResponse(BaseModel):
    """Response for Q&A endpoint"""
    question: str
    answer: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is this document about?",
                "answer": "This document discusses..."
            }
        }


class FileListResponse(BaseModel):
    """Response for file listing"""
    files: List[str]
    count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "files": ["document1.pdf", "document2.pdf"],
                "count": 2
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "1.0.0"
            }
        }
