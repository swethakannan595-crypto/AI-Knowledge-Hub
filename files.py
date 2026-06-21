from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import shutil
import os

from app.db.database import get_db
from app.models.document import Document
from app.services.rag import add_document_to_vectorstore, delete_document_from_vectorstore

router = APIRouter(tags=["files"])
UPLOAD_DIR = "app/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def process_document(file_path: str, filename: str, doc_id: int):
    """Runs in the background after the upload response is already sent."""
    from app.db.database import SessionLocal
    db = SessionLocal()
    try:
        chunk_ids = add_document_to_vectorstore(file_path, filename=filename)
        doc = db.query(Document).filter(Document.id == doc_id).first()
        if doc:
            doc.chroma_ids = ",".join(chunk_ids) if chunk_ids else ""
            db.commit()
    except Exception as e:
        print(f"Background processing error: {e}")
    finally:
        db.close()


@router.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    doc = Document(filename=file.filename, file_path=file_path, chroma_ids="")
    db.add(doc)
    db.commit()
    db.refresh(doc)

    background_tasks.add_task(process_document, file_path, file.filename, doc.id)

    return {"message": f"'{file.filename}' uploaded — processing in background", "id": doc.id}


@router.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(Document.uploaded_at.desc()).all()
    return [
        {"id": d.id, "filename": d.filename, "uploaded_at": d.uploaded_at.isoformat() if d.uploaded_at else None}
        for d in docs
    ]


@router.delete("/documents/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    if doc.chroma_ids:
        try:
            delete_document_from_vectorstore(doc.chroma_ids.split(","))
        except Exception:
            pass

    if doc.file_path and os.path.exists(doc.file_path):
        os.remove(doc.file_path)

    db.delete(doc)
    db.commit()
    return {"message": f"'{doc.filename}' deleted successfully"}