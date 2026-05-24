"""
Document retrieval and QA utilities
"""
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

local_model = None


def get_local_model():
    """Load the local LLM only when the first question is asked."""
    global local_model
    if local_model is not None:
        return local_model

    try:
        local_model = pipeline(
            "text2text-generation",
            model=settings.LLM_MODEL,
            device=settings.DEVICE
        )
        logger.info(f"Successfully loaded LLM model: {settings.LLM_MODEL}")
        return local_model
    except Exception as e:
        logger.error(f"Error loading LLM model: {str(e)}")
        return None


def get_relevant_context(question: str) -> str:
    """
    Retrieve relevant context for a question using vector similarity search.
    
    Args:
        question: The user's question
        
    Returns:
        Relevant context from stored documents
        
    Raises:
        Exception: If retrieval fails
    """
    try:
        vectordb = Chroma(
            persist_directory=str(settings.CHROMA_STORE_DIR),
            embedding_function=HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        )
        retriever = vectordb.as_retriever(
            search_kwargs={"k": settings.MAX_CONTEXT_DOCS}
        )
        docs = retriever.get_relevant_documents(question)
        context = "\n\n".join([doc.page_content for doc in docs])
        logger.info(f"Retrieved context for question: {question}")
        return context
    except Exception as e:
        logger.error(f"Error retrieving context: {str(e)}")
        raise


def answer_question(question: str) -> str:
    """
    Generate an answer to a question based on retrieved context.
    
    Args:
        question: The user's question
        
    Returns:
        Generated answer
        
    Raises:
        Exception: If answer generation fails
    """
    model = get_local_model()
    if not model:
        logger.error("LLM model not loaded")
        return "Sorry, the language model is not available. Please try again later."
    
    try:
        context = get_relevant_context(question)
        
        if not context.strip():
            logger.warning(f"No relevant context found for question: {question}")
            return "I couldn't find relevant information in the uploaded documents to answer your question."
        
        prompt = (
            "You are a helpful PDF assistant. Answer the user's question using "
            "only the document context below. Be conversational, direct, and "
            "concise. If the answer is not in the context, say that you could "
            "not find it in the uploaded PDF.\n\n"
            f"Document context:\n{context}\n\n"
            f"User question: {question}\n"
            "Assistant answer:"
        )
        
        result = model(
            prompt,
            max_new_tokens=settings.MAX_NEW_TOKENS,
            temperature=settings.TEMPERATURE
        )
        
        answer = result[0]['generated_text']
        logger.info(f"Generated answer for question: {question}")
        return answer
        
    except Exception as e:
        logger.error(f"Error generating answer: {str(e)}")
        return "Sorry, I couldn't generate a response. Please try again."


def format_chat_history(history: list[dict]) -> str:
    lines = []
    for item in history[-8:]:
        speaker = "User" if item["role"] == "user" else "Assistant"
        lines.append(f"{speaker}: {item['content']}")
    return "\n".join(lines)


def generate_chat_response(message: str, history: list[dict] | None = None) -> str:
    """
    Generate a general chatbot response without using document retrieval.
    """
    model = get_local_model()
    if not model:
        logger.error("LLM model not loaded")
        return "I'm here and ready to help. Ask me about a PDF, or just tell me what you want to work on."

    try:
        chat_history = format_chat_history(history or [])
        history_block = f"Recent conversation:\n{chat_history}\n\n" if chat_history else ""
        prompt = (
            "You are a friendly, helpful chatbot inside a PDF assistant app. "
            "Reply naturally to the user. Do not mention PDF content unless the "
            "user asks about a document.\n\n"
            f"{history_block}"
            f"User: {message}\n"
            "Assistant:"
        )
        result = model(
            prompt,
            max_new_tokens=min(settings.MAX_NEW_TOKENS, 160),
            temperature=settings.TEMPERATURE
        )
        answer = result[0]["generated_text"].strip()
        return answer or "I'm here. What would you like to chat about?"
    except Exception as e:
        logger.error(f"Error generating chat response: {str(e)}")
        return "I'm here. What would you like to chat about?"
