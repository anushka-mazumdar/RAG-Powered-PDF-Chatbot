
# 📚 RAG-Powered PDF Chatbot (Professional Uvicorn Edition)

A production-ready **Retrieval-Augmented Generation (RAG)** based conversational AI application that answers questions about PDF documents using **FastAPI** and **Uvicorn**. This project demonstrates professional software engineering practices with a clean, scalable architecture.

---

## 🚀 Features

- 📄 **PDF Upload & Processing** - Upload PDFs and automatically extract and embed text
- 🤖 **Intelligent Q&A** - Ask context-aware questions using RAG with local LLMs
- 🔄 **Vector Search** - Fast semantic search using Chroma vector database
- 🎨 **Interactive Frontend** - Clean web interface for document management
- 📋 **Professional Structure** - Industry-standard FastAPI project layout
- 🏥 **Health Checks** - Built-in health monitoring endpoints
- 🚀 **Production Ready** - Optimized for Uvicorn deployment
- 📦 **Docker Ready** - Includes Dockerfile and docker-compose

---

## 🏗️ Professional Architecture

```
app/
├── api/                    # API routes and versioning
│   ├── v1/
│   │   ├── endpoints/
│   │   │   ├── pdf.py     # PDF upload/management routes
│   │   │   └── qa.py      # Q&A endpoint
│   │   └── router.py      # v1 API router
│   └── health.py          # Health check endpoint
├── core/                  # Configuration & constants
│   ├── config.py         # Settings management
│   └── constants.py      # App constants
├── services/             # Business logic layer
│   ├── pdf_service.py   # PDF processing
│   └── qa_service.py    # Q&A logic
├── schemas/              # Pydantic models
│   └── response.py      # API response models
├── utils/                # Utilities & helpers
│   ├── parser.py        # PDF text extraction
│   ├── embedder.py      # Document embedding
│   └── retriever.py     # RAG retrieval & QA
└── main.py              # FastAPI app factory
```

---

## 🧠 Tech Stack

| Component     | Technology |
|---------------|------------|
| **Framework** | FastAPI + Uvicorn |
| **API Docs** | Auto-generated Swagger/OpenAPI |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) |
| **Vector DB** | ChromaDB (persistent) |
| **LLM** | Flan-T5 (local inference) |
| **PDF Parsing** | PyPDF2 |
| **Data Validation** | Pydantic v2 |
| **Configuration** | Python-dotenv |
| **Containerization** | Docker & docker-compose |

---

## 📋 Prerequisites

- Python 3.11+
- Virtual environment (venv or conda)
- 4GB+ RAM (for running local LLM)
- ~2GB disk space (for models cache)

---

## ⚙️ Installation & Setup

### 1. **Navigate to Project**
```bash
cd RAG-Powered-PDF-Chatbot
```

### 2. **Create Virtual Environment**

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4. **Configure Environment (Optional)**
```bash
# Copy example env file
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Edit .env if you want custom settings
# Default settings are production-ready
```

---

## 🚀 Running the Application

### **Option 1: Development Mode (with auto-reload)**
```bash
python run.py
```

### **Option 2: Production Mode (Single Worker)**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### **Option 3: Production Mode (Multiple Workers)**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### **Option 4: Docker Compose**
```bash
docker-compose up --build
```

---

## 🌐 Access the Application

- **Web UI:** http://localhost:8000/
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 📡 API Endpoints

### Health & Status
```
GET /health                    → Check application health
```

### PDF Management (v1)
```
POST /api/v1/pdf/upload       → Upload and embed PDF
GET /api/v1/pdf/uploads       → List uploaded files
DELETE /api/v1/pdf/uploads/{filename} → Delete a file
```

### Question Answering (v1)
```
POST /api/v1/qa/ask           → Ask a question
```

---

## ⚙️ Environment Variables

Edit `.env` file to customize:

```env
# Server Configuration
DEBUG=True                          # Development mode
HOST=0.0.0.0                        # Bind address
PORT=8000                           # Port number

# Model Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2   # HuggingFace model
LLM_MODEL=google/flan-t5-small     # Language model
DEVICE=-1                           # -1=CPU, 0+=GPU

# RAG Tuning
MAX_CONTEXT_DOCS=3                  # Context documents
MAX_NEW_TOKENS=256                  # Response length
TEMPERATURE=0.3                     # Creativity (0.0-1.0)
```

---

## 📦 Project Highlights

✅ **Professional Structure** - Clean separation of concerns (api, services, utils)  
✅ **API Versioning** - Ready for v2, v3 routes  
✅ **Pydantic Models** - Strong type hints & validation  
✅ **Configuration Management** - Environment-based settings  
✅ **Logging** - Comprehensive application logging  
✅ **Error Handling** - Custom HTTP exceptions  
✅ **CORS Support** - Frontend integration ready  
✅ **Uvicorn Ready** - Production ASGI server  
✅ **Docker Support** - Container deployment included  
✅ **Health Checks** - Monitoring endpoints  

---

## 🧪 Testing

Run unit tests:
```bash
pytest tests/ -v
```

---

## 📊 Performance Tips

- **GPU Support:** Set `DEVICE=0` in `.env` (if CUDA available)
- **Multiple Workers:** Use `--workers 4` for production
- **Caching:** First request downloads models (~1-2GB)
- **Context Size:** Adjust `MAX_CONTEXT_DOCS` to balance quality/speed

---

## 🐳 Docker Deployment

### Build Image
```bash
docker build -t rag-chatbot:latest .
```

### Run Container
```bash
docker run -p 8000:8000 -v ./uploads:/app/uploads rag-chatbot:latest
```

### Using Docker Compose
```bash
docker-compose up -d
```

---

## 📚 Directory Walkthrough

| Directory | Purpose |
|-----------|---------|
| `app/api/` | RESTful API endpoints & routers |
| `app/services/` | Business logic & data operations |
| `app/utils/` | Helper functions (parsing, embedding, retrieval) |
| `app/core/` | Configuration & constants |
| `app/schemas/` | Pydantic request/response models |
| `frontend/` | Static HTML/CSS/JS UI |
| `uploads/` | Uploaded PDF storage |
| `chroma_store/` | Vector database persistence |
| `tests/` | Unit & integration tests |

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| `Port 8000 already in use` | Change `PORT` in `.env` or use `--port 8001` |
| `Model download fails` | Check internet, try `pip install -U transformers` |
| `Out of memory` | Use smaller models or reduce `MAX_NEW_TOKENS` |
| `Chroma errors` | Delete `chroma_store/` and restart |
| `CORS errors` | Check `CORS_ORIGINS` in `app/core/config.py` |

---

## 🌟 Future Enhancements

- [ ] Async embedding pipeline
- [ ] User authentication & sessions
- [ ] Database persistence (PostgreSQL)
- [ ] Redis caching layer
- [ ] Advanced RAG techniques
- [ ] Frontend UI improvements
- [ ] API rate limiting
- [ ] Monitoring & metrics (Prometheus)

---

## 📝 License

MIT License - Feel free to use and modify

---

## 👨‍💻 Built By

**Anushka Mazumdar** - Professional RAG Implementation with FastAPI & Uvicorn

Questions? Issues? Contributions welcome! 🚀