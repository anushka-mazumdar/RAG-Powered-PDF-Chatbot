"""
PDF parsing utilities
"""
from PyPDF2 import PdfReader
import logging

logger = logging.getLogger(__name__)


def load_pdf(path: str) -> str:
    """
    Load and extract text from a PDF file.
    
    Args:
        path: Path to the PDF file
        
    Returns:
        Extracted text from the PDF
        
    Raises:
        Exception: If PDF reading fails
    """
    try:
        reader = PdfReader(path)
        page_text = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(page_text).strip()
        if not text:
            raise ValueError("No readable text found in this PDF.")
        logger.info(f"Successfully loaded PDF: {path}")
        return text
    except Exception as e:
        logger.error(f"Error loading PDF {path}: {str(e)}")
        raise
