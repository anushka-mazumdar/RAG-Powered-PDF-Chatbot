"""
Document retrieval and QA utilities
"""
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Load local text-to-text model
try:
    local_model = pipeline(
        "text2text-generation",
        model=settings.LLM_MODEL,
        device=settings.DEVICE
    )
    logger.info(f"Successfully loaded LLM model: {settings.LLM_MODEL}")
except Exception as e:
    logger.error(f"Error loading LLM model: {str(e)}")
    local_model = None


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
        retriever = vectordb.as_retriever()
        docs = retriever.get_relevant_documents(question)
        context = "\n".join([
            doc.page_content for doc in docs[:settings.MAX_CONTEXT_DOCS]
        ])
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
    if not local_model:
        logger.error("LLM model not loaded")
        return "Sorry, the language model is not available. Please try again later."
    
    try:
        context = get_relevant_context(question)
        
        if not context.strip():
            logger.warning(f"No relevant context found for question: {question}")
            return "I couldn't find relevant information in the uploaded documents to answer your question."
        
        prompt = (
            f"Answer the following question based on the context:\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {question}\n"
            f"Answer:"
        )
        
        result = local_model(
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
