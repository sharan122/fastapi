import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from pdfminer.high_level import extract_text
from docx import Document
import openai
from app.database import get_db
from app.routes.users import get_current_user
from werkzeug.utils import secure_filename  # Prevents unsafe file names

router = APIRouter(prefix="/rag", tags=["RAG Pipeline"])


openai.api_key = os.getenv("OPENAI_API_KEY")


DOCUMENTS = {}

def extract_text_from_file(file_path: str) -> str:
    """Extract text from PDF, TXT, or DOCX files."""
    try:
        if file_path.endswith(".pdf"):
            return extract_text(file_path)
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
        elif file_path.endswith(".docx"):
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@router.post("/upload/")
async def upload_file(file: UploadFile = File(...), current_user=Depends(get_current_user)):
    """Upload a document and extract text (JWT Protected)."""
    
    # Secure filename to prevent path traversal attacks
    filename = secure_filename(file.filename)
    file_path = os.path.join("uploads", filename)

    os.makedirs("uploads", exist_ok=True)  # Ensure the upload folder exists
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        text = extract_text_from_file(file_path)
        DOCUMENTS[filename] = text

        return {"message": "File uploaded successfully", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query/")
async def query_document(filename: str = Form(...), question: str = Form(...), current_user=Depends(get_current_user)):
    """Query the uploaded document using GPT-4o-mini (JWT Protected)."""
    
    if filename not in DOCUMENTS:
        raise HTTPException(status_code=404, detail="File not found")

    document_text = DOCUMENTS[filename]
    prompt = f"Document:\n{document_text}\n\nUser Question: {question}\nAnswer:"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI answering questions based on a document."},
                {"role": "user", "content": prompt}
            ]
        )
        return {"answer": response["choices"][0]["message"]["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying AI: {str(e)}")
