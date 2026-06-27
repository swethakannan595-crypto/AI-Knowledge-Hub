from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.document import Document
from app.models.user import User

router = APIRouter(tags=["search"])


@router.get("/search")
def search(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    docs = db.query(Document).filter(Document.filename.ilike(f"%{q}%")).all()
    users = db.query(User).filter(
        (User.username.ilike(f"%{q}%")) | (User.email.ilike(f"%{q}%"))
    ).all()

    return {
        "documents": [{"id": d.id, "filename": d.filename} for d in docs],
        "users": [{"id": u.id, "username": u.username, "email": u.email} for u in users]
    }
