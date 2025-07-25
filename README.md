
# 📚 RAG-Powered PDF Chatbot using Transformers, LangChain & FastAPI

A private document-based chatbot that allows users to upload their own PDF files and ask questions directly based on their content. The chatbot uses **Retrieval-Augmented Generation (RAG)** to generate accurate answers by searching only within your uploaded documents — not the internet.

---

## 🚀 Features

- 📂 Upload your own PDF documents
- 💬 Ask natural language questions about them
- 🧠 Uses **LangChain + ChromaDB** for retrieval
- 🤖 Answered using local **Transformers (e.g., T5 or Mistral)**
- ⚡ FastAPI backend for APIs
- 🔐 Firebase integration (frontend only, optional)
- 🌐 Frontend with Firebase SDK (planned for next phase)

---

## 🧠 Tech Stack

| Layer         | Technology |
|---------------|------------|
| Embeddings    | HuggingFace MiniLM (`all-MiniLM-L6-v2`) |
| Vector Store  | ChromaDB (local persistent store) |
| LLM           | Local Transformer via `transformers` pipeline (`flan-t5-base`, `mistral-7b-instruct`, etc.) |
| Retrieval     | Custom retrieval + prompt construction |
| PDF Parsing   | PyPDF2 |
| Backend       | FastAPI + Uvicorn |
| Environment   | Python 3.10+ |
| Frontend Auth | Firebase (optional) |

---

## 📁 Project Structure

```
pdf-chatbot/
├── backend/
│   ├── chroma_store/             ← Chroma vector DB files
│   ├── uploads/                  ← Uploaded PDFs
│   ├── utils/
│   │   ├── embedder.py           ← Embedding generator using MiniLM
│   │   ├── parser.py             ← PDF text extractor
│   │   └── retriever.py          ← Vector search + local transformer pipeline
│   ├── app.py                    ← FastAPI backend (file upload + chat)
│   └── .env                      ← (Optional) reserved for secrets
│
├── firebase/
│   └── functions/
│       └── index.js              ← Placeholder for Firebase Functions (frontend)
│
├── frontend/                     ← React + Firebase SDK planned
├── requirements.txt              ← Python backend dependencies
├── package.json                  ← Node dependencies (for Firebase/Frontend)
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
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` isn't ready, run:

```bash
pip install fastapi uvicorn python-multipart langchain langchain-community chromadb sentence-transformers PyPDF2 transformers
pip freeze > requirements.txt
```

---

## ▶️ Running the Server

```bash
uvicorn app:app --reload
```

Open your browser:  
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
Use Swagger UI to:
- Upload `.pdf` file via `/upload`
- Ask a question via `/ask`

---

## 📌 Notes
- Works best with **text-based PDFs** (not scanned image PDFs)
- Uses **LangChain only for embeddings + vector DB**
- Answers are generated using **local Transformer models** via HuggingFace `pipeline()`
- Can switch between models like `flan-t5-base`, `mistral-7b-instruct`, or `t5-small` easily
---

⚠️ Note: This project is currently a work in progress. New features like Firebase integration and a frontend interface are actively being developed.

---
## 🙋‍♂️ Author

Built with ❤️ by Anushka Mazumdar  
Feel free to fork, contribute, or reach out for questions!
