"""
PDF processing service
"""
import os
import shutil
from pathlib import Path
from fastapi import UploadFile
from app.core.config import settings
from app.utils.parser import load_pdf
from app.utils.embedder import embed_docs
import logging

logger = logging.getLogger(__name__)


class PDFService:
    """Service for handling PDF upload and processing"""
    
    @staticmethod
    async def upload_and_process(file: UploadFile) -> dict:
        """
        Upload a PDF file and embed its content.
        
        Args:
            file: The uploaded file
            
        Returns:
            Dictionary with upload status and message
            
        Raises:
            Exception: If processing fails
        """
        try:
            # Save uploaded file
            file_path = settings.UPLOAD_DIR / file.filename
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            logger.info(f"File saved: {file_path}")
            
            # Load and embed
            text = load_pdf(str(file_path))
            embed_docs([text])
            
            logger.info(f"Successfully processed PDF: {file.filename}")
            
            return {
                "success": True,
                "filename": file.filename,
                "message": f"{file.filename} uploaded and embedded successfully."
            }
            
        except Exception as e:
            logger.error(f"Error processing PDF: {str(e)}")
            raise
    
    @staticmethod
    def list_uploaded_files() -> dict:
        """
        List all uploaded PDF files.
        
        Returns:
            Dictionary with file list and count
            
        Raises:
            Exception: If listing fails
        """
        try:
            files = os.listdir(settings.UPLOAD_DIR)
            # Filter only PDF files
            pdf_files = [f for f in files if f.lower().endswith('.pdf') and 
                        os.path.isfile(settings.UPLOAD_DIR / f)]
            
            logger.info(f"Listed {len(pdf_files)} uploaded files")
            
            return {
                "files": pdf_files,
                "count": len(pdf_files)
            }
            
        except Exception as e:
            logger.error(f"Error listing files: {str(e)}")
            raise
    
    @staticmethod
    def delete_file(filename: str) -> dict:
        """
        Delete an uploaded file.
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            Dictionary with deletion status
            
        Raises:
            Exception: If deletion fails
        """
        try:
            file_path = settings.UPLOAD_DIR / filename
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {filename}")
            
            os.remove(file_path)
            logger.info(f"Deleted file: {filename}")
            
            return {
                "success": True,
                "message": f"{filename} deleted successfully."
            }
            
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            raise
