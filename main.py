from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from app.db.database import engine
from app.models import user, document
import os

user.Base.metadata.create_all(bind=engine)
document.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    with open(path, "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/search")
async def search(q: str = ""):
    from app.db.database import SessionLocal
    from app.models.user import User
    from app.services.rag import get_all_documents
    db = SessionLocal()
    try:
        users = db.query(User).filter(
            User.username.ilike(f"%{q}%") | User.email.ilike(f"%{q}%")
        ).all() if q else []
        docs = get_all_documents()
        filtered_docs = [d for d in docs if q.lower() in d.lower()] if q else docs
        return {
            "users": [{"id": u.id, "username": u.username, "email": u.email} for u in users],
            "documents": filtered_docs
        }
    finally:
        db.close()

from app.api import users, chat, files
app.include_router(users.router)
app.include_router(chat.router)
app.include_router(files.router)
