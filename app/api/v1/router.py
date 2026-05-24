"""
API v1 router - combines all v1 endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import pdf, qa

router = APIRouter()

# Include routers from endpoints
router.include_router(pdf.router)
router.include_router(qa.router)
