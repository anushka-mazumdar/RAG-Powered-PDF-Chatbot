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
        text = "\n".join([page.extract_text() for page in reader.pages])
        logger.info(f"Successfully loaded PDF: {path}")
        return text
    except Exception as e:
        logger.error(f"Error loading PDF {path}: {str(e)}")
        raise
