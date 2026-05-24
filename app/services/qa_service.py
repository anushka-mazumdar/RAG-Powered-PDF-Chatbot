"""
Question Answering service
"""
from app.utils.retriever import answer_question, generate_chat_response, get_relevant_context
from app.services.pdf_service import PDFService
import logging
import re

logger = logging.getLogger(__name__)


SMALL_TALK_RESPONSES = {
    "hi": "Hi! I'm here. Upload a PDF when you're ready, or ask me anything you want to work through.",
    "hello": "Hello! What are we working on today?",
    "hey": "Hey! Send me a question, or upload a PDF and I'll help you explore it.",
    "thanks": "You're welcome.",
    "thank you": "You're welcome.",
    "bye": "Bye! Come back whenever you want to continue.",
}

DOCUMENT_HINTS = {
    "pdf", "document", "paper", "article", "file", "uploaded", "context",
    "according", "summarize", "summary", "explain this", "what does this",
    "in this", "from this", "based on", "the text", "the author", "section",
    "abstract", "conclusion", "methodology", "dataset", "results"
}


def normalize_message(message: str) -> str:
    return re.sub(r"\s+", " ", message.strip().lower())


def get_small_talk_response(message: str) -> str | None:
    normalized = normalize_message(message)
    cleaned = re.sub(r"[^a-z0-9\s]", "", normalized)
    return SMALL_TALK_RESPONSES.get(cleaned)


def is_document_question(message: str) -> bool:
    normalized = normalize_message(message)
    if any(hint in normalized for hint in DOCUMENT_HINTS):
        return True
    question_words = ("what", "why", "how", "when", "where", "who", "which")
    return normalized.startswith(question_words) and len(normalized.split()) > 4


def has_uploaded_documents() -> bool:
    try:
        return PDFService.list_uploaded_files()["count"] > 0
    except Exception:
        logger.warning("Could not check uploaded documents", exc_info=True)
        return False


def clean_history(history: list | None) -> list[dict]:
    if not isinstance(history, list):
        return []

    cleaned = []
    for item in history[-8:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role in {"user", "assistant"} and isinstance(content, str) and content.strip():
            cleaned.append({"role": role, "content": content.strip()[:1000]})
    return cleaned


def format_history(history: list[dict]) -> str:
    lines = []
    for item in history:
        speaker = "User" if item["role"] == "user" else "Assistant"
        lines.append(f"{speaker}: {item['content']}")
    return "\n".join(lines)


def rewrite_followup(question: str, history: list[dict]) -> str:
    normalized = normalize_message(question)
    if not history or len(normalized.split()) > 4:
        return question

    vague_followups = {
        "why", "how", "explain", "explain more", "tell me more",
        "what about it", "what does that mean", "continue"
    }
    if normalized not in vague_followups:
        return question

    return f"{format_history(history[-4:])}\nUser follow-up: {question}"


class QAService:
    """Service for handling question answering"""
    
    @staticmethod
    def answer(question: str, history: list | None = None) -> dict:
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
            
            cleaned_history = clean_history(history)
            small_talk = get_small_talk_response(question)
            if small_talk:
                answer = small_talk
            elif is_document_question(question):
                if has_uploaded_documents():
                    answer = answer_question(rewrite_followup(question, cleaned_history))
                else:
                    answer = "Upload a PDF first, then ask me questions about it. I can also chat normally while you get the document ready."
            else:
                answer = generate_chat_response(question, cleaned_history)
            
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
