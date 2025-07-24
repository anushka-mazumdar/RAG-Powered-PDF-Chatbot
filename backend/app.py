from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from utils.parser import load_pdf
from utils.embedder import embed_docs
from utils.retriever import get_qa_bot
import os
import shutil

app = FastAPI()

# Allow CORS from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File upload folder
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "PDF Chatbot API is running..."}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract & embed
    text = load_pdf(file_path)
    embed_docs([text])  # Embeds into ChromaDB

    return {"message": f"{file.filename} uploaded and embedded successfully."}

@app.post("/ask")
async def ask_question(question: str = Form(...)):
    qa = get_qa_bot()
    response = qa.run(question)
    return {"answer": response}

