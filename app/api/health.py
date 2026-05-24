"""
Health check endpoints
"""
from fastapi import APIRouter
from app.schemas.response import HealthResponse
from app.core.config import settings

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    """
    return HealthResponse(
        status="healthy",
        version=settings.API_VERSION
    )
