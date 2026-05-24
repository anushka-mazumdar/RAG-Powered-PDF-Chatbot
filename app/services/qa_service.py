"""
Question Answering service
"""
from app.utils.retriever import answer_question, get_relevant_context
import logging

logger = logging.getLogger(__name__)


class QAService:
    """Service for handling question answering"""
    
    @staticmethod
    def answer(question: str) -> dict:
        """
        Generate an answer to a user question.
        
        Args:
            question: The user's question
            
        Returns:
            Dictionary with question and answer
            
        Raises:
            Exception: If answer generation fails
        """
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        
        try:
            logger.info(f"Processing question: {question}")
            
            answer = answer_question(question)
            
            return {
                "success": True,
                "question": question,
                "answer": answer
            }
            
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            raise
    
    @staticmethod
    def get_context(question: str) -> dict:
        """
        Get relevant context for a question without generating an answer.
        
        Args:
            question: The user's question
            
        Returns:
            Dictionary with question and context
            
        Raises:
            Exception: If retrieval fails
        """
        if not question or not question.strip():
            raise ValueError("Question cannot be empty")
        
        try:
            logger.info(f"Retrieving context for: {question}")
            
            context = get_relevant_context(question)
            
            return {
                "success": True,
                "question": question,
                "context": context
            }
            
        except Exception as e:
            logger.error(f"Error retrieving context: {str(e)}")
            raise
