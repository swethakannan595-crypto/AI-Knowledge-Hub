from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os

from app.db.database import engine
from app.models import user, document

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


@app.get("/debug/env")
async def debug_env():
    groq_key = os.getenv("GROQ_API_KEY")
    return {
        "groq_key_found": groq_key is not None,
        "groq_key_preview": groq_key[:10] + "..." if groq_key else "NOT FOUND"
    }


from app.api import users, chat, files, search
app.include_router(users.router)
app.include_router(chat.router)
app.include_router(files.router)
app.include_router(search.router)