"""
PDF upload and management endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import PDFService
from app.schemas.response import SuccessResponse, ErrorResponse, FileListResponse
import logging
import traceback

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/pdf", tags=["pdf"])


@router.post("/upload", response_model=SuccessResponse)
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload and process a PDF file.
    
    - **file**: PDF file to upload
    """
    try:
        result = await PDFService.upload_and_process(file)
        return SuccessResponse(
            message=result["message"],
            data={"filename": result["filename"]}
        )
    except Exception as e:
        logger.error(f"Error uploading PDF: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=400,
            detail=f"Failed to upload PDF: {str(e)}"
        )


@router.get("/uploads", response_model=FileListResponse)
async def list_uploads():
    """
    List all uploaded PDF files.
    """
    try:
        result = PDFService.list_uploaded_files()
        return FileListResponse(
            files=result["files"],
            count=result["count"]
        )
    except Exception as e:
        logger.error(f"Error listing uploads: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list uploads: {str(e)}"
        )


@router.delete("/uploads/{filename}")
async def delete_upload(filename: str):
    """
    Delete an uploaded PDF file.
    
    - **filename**: Name of the file to delete
    """
    try:
        result = PDFService.delete_file(filename)
        return SuccessResponse(message=result["message"])
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete file: {str(e)}"
        )
