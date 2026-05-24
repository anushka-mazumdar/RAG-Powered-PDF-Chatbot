"""
Document embedding utilities
"""
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


def embed_docs(docs: list, persist_path: str = None) -> Chroma:
    """
    Embed documents and store them in Chroma vector database.
    
    Args:
        docs: List of documents (text strings) to embed
        persist_path: Path to persist the vector database (uses settings if None)
        
    Returns:
        Chroma vector database instance
        
    Raises:
        Exception: If embedding fails
    """
    if persist_path is None:
        persist_path = str(settings.CHROMA_STORE_DIR)
    
    try:
        embedding = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
        vectordb = Chroma.from_texts(
            docs, 
            embedding=embedding, 
            persist_directory=persist_path
        )
        vectordb.persist()
        logger.info(f"Successfully embedded {len(docs)} documents")
        return vectordb
    except Exception as e:
        logger.error(f"Error embedding documents: {str(e)}")
        raise
