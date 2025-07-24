
# 📚 RAG-Powered PDF Chatbot using LangChain, ChromaDB & FastAPI

A private document-based chatbot that allows users to upload their own PDF files and ask questions directly based on their content. The chatbot uses **Retrieval-Augmented Generation (RAG)** to generate accurate answers by searching only within your uploaded content — not the internet.

---

## 🚀 Features

- 📂 Upload your own PDF documents
- 💬 Ask natural language questions about them
- 🧠 Uses **LangChain + ChromaDB** for retrieval
- 🤖 Powered by **Hugging Face LLMs (Flan-T5)**
- ⚡ Backend with **FastAPI**
- 🔐 Firebase integration (coming soon): authentication, secure storage
- 🌐 Frontend (React + Firebase SDK) planned in next phase

---

## 🧠 Tech Stack

| Layer         | Technology |
|---------------|------------|
| Embeddings    | HuggingFace MiniLM (`all-MiniLM-L6-v2`) |
| Vector Store  | ChromaDB (Local persistent store) |
| LLM           | `flan-t5-base` from Hugging Face Inference API |
| Chain         | LangChain `RetrievalQA` |
| PDF Parsing   | PyPDF2 |
| Backend       | FastAPI + Uvicorn |
| Environment   | Python 3.10+ |
| Auth & Storage| Firebase (to be added in Stage 4) |

---

## 📁 Project Structure

```
chatbot/
├── backend/
│   ├── __pycache__/              ← Python cache
│   ├── chroma_store/             ← Chroma vector DB files
│   ├── uploads/                  ← Uploaded PDFs
│   ├── utils/
│   │   ├── __pycache__/
│   │   ├── embedder.py           ← Embedding generator
│   │   ├── parser.py             ← PDF text extractor
│   │   └── retriever.py          ← LangChain QA chain with Hugging Face
│   ├── app.py                    ← FastAPI backend
│   └── .env                      ← Hugging Face API key 
│
├── firebase/
│   └── functions/
│       └── index.js              ← Placeholder for Firebase Functions (planned)
│
├── frontend/                     ← Frontend app (React planned)
│
├── requirements.txt              ← Python dependencies
├── package.json                  ← Node project dependencies (for Firebase/Frontend)
└── .gitignore                    ← Git ignored files/folders
```

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/pdf-rag-chatbot.git
cd pdf-rag-chatbot/backend
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` isn't created yet, run:
```bash
pip install fastapi uvicorn python-multipart langchain langchain-community chromadb huggingface_hub python-dotenv PyPDF2 sentence-transformers
pip freeze > requirements.txt
```

### 4. Add Hugging Face API Key

Create a `.env` file in the `backend/` folder:

```
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

Get your token from: https://huggingface.co/settings/tokens

---

## ▶️ Running the Server

```bash
uvicorn app:app --reload
```

Go to: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
Use Swagger UI to:
- Upload a `.pdf` file via `/upload`
- Ask questions via `/ask`

---

## 📌 Notes

- Works best with **text-based PDFs** (not scanned images)
- Uses local ChromaDB to persist vectors
- LLM queries are sent to Hugging Face via API
- You can swap `flan-t5-base` with other supported models (like `tiiuae/falcon-7b-instruct`)

---
⚠️ Note: This project is currently a work in progress. New features like Firebase integration and a frontend interface are actively being developed.
---
## 🙋‍♂️ Author

Built with ❤️ by Anushka Mazumdar  
Feel free to fork, contribute, or reach out for questions!
