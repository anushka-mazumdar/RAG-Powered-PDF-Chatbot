"""
Question Answering endpoints
"""
from fastapi import APIRouter, Form, HTTPException
from app.services.qa_service import QAService
from app.schemas.response import AnswerResponse
import logging
import traceback
import json

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/qa", tags=["qa"])


@router.post("/ask", response_model=AnswerResponse)
async def ask_question(question: str = Form(...), history: str = Form("")):
    """
    Ask a question and get an answer based on uploaded documents.
    
    - **question**: The question to ask
    """
    try:
        logger.info(f"Received question: {question}")
        try:
            parsed_history = json.loads(history) if history else []
        except json.JSONDecodeError:
            parsed_history = []
        result = QAService.answer(question, parsed_history)
        return AnswerResponse(
            question=result["question"],
            answer=result["answer"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer: {str(e)}"
        )
