"""
Entry point for running the application with Uvicorn
"""
import uvicorn
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info(f"Starting {settings.API_TITLE}")
    logger.info(f"Server running at http://{settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )
