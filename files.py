import os
import shutil
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from app.services.rag import add_document, get_all_documents, delete_document

router = APIRouter(tags=["files"])
UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_document(file_path: str, filename: str):
    try:
        add_document(file_path, filename)
        print(f"Successfully indexed: {filename}")
    except Exception as e:
        print(f"Error processing {filename}: {e}")

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks()
):
    # Only allow PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    background_tasks.add_task(process_document, file_path, file.filename)

    return {
        "message": f"'{file.filename}' uploaded and indexing started!",
        "filename": file.filename
    }

@router.get("/documents")
async def list_documents():
    try:
        indexed = get_all_documents()
        all_files = []
        if os.path.exists(UPLOAD_DIR):
            all_files = [f for f in os.listdir(UPLOAD_DIR) if f.lower().endswith(".pdf")]
        all_docs = list(set(indexed + all_files))
        result = []
        for i, filename in enumerate(all_docs):
            result.append({
                "id": i,
                "filename": filename,
                "indexed": filename in indexed
            })
        return {"documents": result, "count": len(result)}
    except Exception as e:
        return {"documents": [], "count": 0}

@router.delete("/documents/{filename:path}")
async def remove_document(filename: str):
    delete_document(filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
    return {"message": f"'{filename}' deleted successfully"}
