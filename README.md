🧠 Index — AI-Powered Knowledge Management System

Chat with your documents using Retrieval-Augmented Generation (RAG), FastAPI, and Llama 3.1


<img width="947" height="465" alt="image" src="https://github.com/user-attachments/assets/fb71f250-c84f-4755-80e7-173c591b9601" />

<img width="939" height="463" alt="image" src="https://github.com/user-attachments/assets/770f6d1e-f1b9-4c06-be01-3576753beb70" />

<img width="957" height="469" alt="image" src="https://github.com/user-attachments/assets/804998f8-2922-487e-8aa0-5d60c2e2aa2c" />

<img width="948" height="471" alt="image" src="https://github.com/user-attachments/assets/3d6c1715-cf00-49a3-b6a1-d342b0f44dbe" />

</div>

📖 Overview

Index is a full-stack AI Knowledge Management System that lets users upload PDF documents and have natural-language conversations with their content. Built with FastAPI and powered by Retrieval-Augmented Generation (RAG), it combines a vector database, semantic search, and a fast open-source LLM to deliver accurate, context-grounded answers — not hallucinations.

This project demonstrates production-style backend engineering: authentication, database design, vector search, LLM orchestration, and a clean API surface — the kind of system used in enterprise knowledge bases, internal copilots, and document-intelligence tools.


✨ Features

🔐 Authentication & Security


JWT-based login and registration system
Bcrypt password hashing
Email format validation and password strength rules (min. 8 chars, uppercase, number)
Persistent sessions via secure token storage


🤖 AI-Powered Q&A (RAG Pipeline)


Natural-language chat interface powered by Llama 3.1 (via Groq) — sub-second inference
Retrieval-Augmented Generation: answers are grounded in your uploaded documents, not just model memory
Conversation history maintained across a session
Quick-action prompts: Summarize Documents, Extract Key Topics, Generate Report, Suggest Questions
Visual indicator showing when an answer was sourced from your documents


📄 Smart Document Indexing


PDF upload with automatic text extraction (pypdf)
Recursive text chunking for optimal retrieval (langchain-text-splitters)
Sentence-transformer embeddings (all-MiniLM-L6-v2)
Vector storage and semantic similarity search via ChromaDB
Live document index with status tracking


👥 User Management


User registration and role-aware access
Admin-visible user directory
Multi-user support over local network (--host 0.0.0.0)


📊 Dashboard & Analytics


Live system stats: total users, indexed documents, session queries
System health readout (backend, database, model, retrieval status)
Quick-action shortcuts to core workflows


🎨 Professional UI


Custom-designed single-page interface (no framework bloat — vanilla HTML/CSS/JS)
Responsive layout, accessible components, smooth state transitions
Built entirely on top of a documented REST API (testable via /docs)



🛠️ Tech Stack

LayerTechnologyBackend FrameworkFastAPI (Python 3.11+)DatabasePostgreSQL + SQLAlchemy ORMVector DatabaseChromaDBEmbeddingssentence-transformers (all-MiniLM-L6-v2)LLM InferenceGroq API — Llama 3.1 8B InstantAuthenticationJWT (python-jose) + bcrypt (passlib)PDF ProcessingpypdfText ChunkingLangChain Text SplittersFrontendHTML5, CSS3, Vanilla JavaScriptServerUvicorn (ASGI)


🏗️ Architecture

┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   Browser   │ ───▶ │   FastAPI    │ ───▶ │   PostgreSQL     │
│  (Vanilla   │      │   Backend    │      │  (Users, Docs)   │
│   JS UI)    │ ◀─── │              │ ◀─── │                  │
└─────────────┘      └──────┬───────┘      └─────────────────┘
                             │
                ┌────────────┼────────────┐
                ▼                         ▼
       ┌─────────────────┐      ┌──────────────────┐
       │    ChromaDB      │      │   Groq API        │
       │  (Vector Store)  │      │  (Llama 3.1 LLM)  │
       └─────────────────┘      └──────────────────┘

RAG Flow: PDF upload → text extraction → chunking → embedding → ChromaDB storage → on query, semantic search retrieves relevant chunks → chunks + question sent to Llama 3.1 → grounded answer returned.


🚀 Getting Started

Prerequisites


Python 3.11+
PostgreSQL (via pgAdmin 4 or CLI)
A free Groq API key


Installation

bash# Clone the repository
git clone https://github.com/yourusername/ai-knowledge-hub.git
cd ai-knowledge-hub

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt

Environment Setup

Create a .env file in the project root:

envDATABASE_URL=postgresql://postgres:yourpassword@localhost/ai_knowledge_hub
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_jwt_secret_key_here

Database Setup

bash# Create the database (via pgAdmin 4 or psql)
CREATE DATABASE ai_knowledge_hub;

Run the Server

bashpython -m uvicorn app.main:app --reload

Visit http://127.0.0.1:8000 to access the app, or http://127.0.0.1:8000/docs for the interactive API documentation.


📁 Project Structure

ai-knowledge-hub/
├── app/
│   ├── main.py                 # FastAPI app entrypoint
│   ├── api/
│   │   ├── users.py            # Auth: register, login, user CRUD
│   │   ├── chat.py             # RAG chat endpoint
│   │   └── files.py            # PDF upload + document listing
│   ├── models/
│   │   ├── user.py             # User ORM model
│   │   └── document.py         # Document ORM model
│   ├── services/
│   │   ├── auth.py             # JWT + password hashing
│   │   └── rag.py              # PDF parsing, embeddings, vector search
│   ├── db/
│   │   └── database.py         # SQLAlchemy engine/session
│   ├── templates/
│   │   └── index.html          # Frontend SPA
│   └── chroma_db/               # Persisted vector store
├── requirements.txt
├── .env
└── README.md


🔑 API Endpoints

MethodEndpointDescriptionPOST/registerCreate a new user accountPOST/loginAuthenticate and receive a JWTGET/usersList all registered usersGET/users/meGet current authenticated userPOST/uploadUpload and index a PDF documentGET/documentsList all indexed documentsPOST/chatSend a question to the RAG-powered assistantGET/chat/historyRetrieve conversation historyDELETE/chat/historyClear conversation history

Full interactive documentation available at /docs (Swagger UI).


🗺️ Roadmap


 Document deletion from vector store
 Full-text search across all documents
 User profile management (change password/email)
 Admin panel with usage analytics
 Persisted chat history per user (database-backed)
 In-browser PDF preview
 Redis caching for repeated queries
 OCR support for scanned documents
 Docker Compose for one-command deployment
 CI/CD + cloud deployment (Railway / Render)



🎯 Skills Demonstrated

LLM Integration · RAG Architecture · Vector Databases · REST API Design · JWT Authentication · Database Modeling (SQLAlchemy) · Semantic Search · Async Python (FastAPI) · Full-Stack Development · Prompt Engineering


📄 License

This project is open source and available under the MIT License.


<div align="center">
Built as a hands-on exploration of production RAG systems — from raw PDF to grounded AI answers.

</div>
