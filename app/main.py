"""
FastAPI application factory and configuration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import logging

from app.core.config import settings
from app.api.v1.router import router as api_v1_router
from app.api.health import router as health_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        debug=settings.DEBUG,
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )
    
    # Mount static files
    app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")
    
    # Include routers
    app.include_router(health_router)
    app.include_router(api_v1_router, prefix=settings.API_PREFIX)
    
    # Serve frontend
    @app.get("/")
    async def root():
        """Serve the frontend index.html"""
        return FileResponse(str(settings.STATIC_DIR / "index.html"))
    
    # Startup event
    @app.on_event("startup")
    async def startup_event():
        logger.info(f"Starting {settings.API_TITLE}")
        logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info(f"Shutting down {settings.API_TITLE}")
    
    return app


# Create the application instance
app = create_app()
