"""
Application configuration and settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get base directory
BASE_DIR = Path(__file__).parent.parent.parent

class Settings:
    """Application settings"""
    
    # API
    API_TITLE = "RAG-Powered PDF Chatbot"
    API_DESCRIPTION = "A conversational AI that answers questions based on uploaded PDF documents"
    API_VERSION = "1.0.0"
    API_PREFIX = "/api/v1"
    
    # Server
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    
    # CORS
    CORS_ORIGINS = ["*"]
    CORS_CREDENTIALS = True
    CORS_METHODS = ["*"]
    CORS_HEADERS = ["*"]
    
    # Paths
    BASE_DIR = BASE_DIR
    UPLOAD_DIR = BASE_DIR / "uploads"
    CHROMA_STORE_DIR = BASE_DIR / "chroma_store"
    STATIC_DIR = BASE_DIR / "frontend" / "static"
    
    # Ensure directories exist
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    CHROMA_STORE_DIR.mkdir(parents=True, exist_ok=True)
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    
    # Models
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    LLM_MODEL = os.getenv("LLM_MODEL", "google/flan-t5-small")
    
    # RAG
    MAX_CONTEXT_DOCS = int(os.getenv("MAX_CONTEXT_DOCS", "3"))
    MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "256"))
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
    
    # Device
    DEVICE = int(os.getenv("DEVICE", "-1"))  # -1 for CPU, 0+ for GPU


settings = Settings()
