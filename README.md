<div align="center">

# 🧠 Index — AI-Powered Knowledge Management System

</div>

Chat with your documents using Retrieval-Augmented Generation (RAG), FastAPI, and Llama 3.1

🔗 Live Demo: https://ai-knowledge-hub-m0k2.onrender.com

Username: testuser
Password: Test1234

Use this username and password 

---

## 📖 Overview

While exploring AI-powered learning tools, I noticed a common challenge: many document assistants support only limited file formats, impose upload restrictions, or require users to switch between multiple tools to work with different types of study material.

I wanted to build a solution that makes learning simpler, more intuitive, and grounded in the user's own knowledge.

**Index — AI Knowledge Hub** is a full-stack AI Knowledge Management System that lets users upload PDF documents and have natural-language conversations with their content. Built on a Retrieval-Augmented Generation (RAG) architecture, it combines semantic search, vector embeddings, and a high-speed LLM to generate accurate, context-aware responses grounded in the uploaded documents — rather than relying solely on the model's general knowledge.

This project demonstrates production-style backend engineering: authentication, database design, vector search, LLM orchestration, and a clean API surface — the kind of system used in enterprise knowledge bases, internal copilots, and document-intelligence tools.

---

## ✨ Features

### 🔐 Authentication & Security

- JWT-based login and registration system
- Bcrypt password hashing
- Email format validation and password strength rules (min. 8 chars, uppercase, number)
- Persistent sessions via secure token storage

### 🤖 AI-Powered Q&A (RAG Pipeline)

- Natural-language chat interface powered by Llama 3.1 (via Groq) — sub-second inference
- Retrieval-Augmented Generation: answers are grounded in your uploaded documents, not just model memory
- Conversation history maintained across a session
- Quick-action prompts: Summarize Documents, Extract Key Topics, Generate Report, Suggest Questions
- Visual indicator showing when an answer was sourced from your documents
  

<img width="931" height="432" alt="Chat interface screenshot" src="https://github.com/user-attachments/assets/cdf80dc4-9dbc-48d5-a9b4-6c300eb976a8" />


### 📄 Smart Document Indexing

- PDF upload with automatic text extraction (pypdf)
- Recursive text chunking for optimal retrieval (langchain-text-splitters)
- Sentence-transformer embeddings (all-MiniLM-L6-v2)
- Vector storage and semantic similarity search via ChromaDB
- Live document index with status tracking


<img width="1860" height="872" alt="Document index screenshot" src="https://github.com/user-attachments/assets/529611b1-b68c-4c7c-8a33-2c73347e74fe" />


### 👥 User Management

- User registration and role-aware access
- Admin-visible user directory
- Multi-user support over local network (`--host 0.0.0.0`)


<img width="1868" height="864" alt="User management screenshot" src="https://github.com/user-attachments/assets/94a6f6fd-94cc-4080-afd0-b3fb12e1bcd2" />


### 📊 Dashboard & Analytics

- Live system stats: total users, indexed documents, session queries
- System health readout (backend, database, model, retrieval status)
- Quick-action shortcuts to core workflows

### 🎨 Professional UI

- Custom-designed single-page interface (no framework bloat — vanilla HTML/CSS/JS)
- Responsive layout, accessible components, smooth state transitions
- Built entirely on top of a documented REST API (testable via `/docs`)
  



---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | FastAPI (Python 3.11+) |
| Database | PostgreSQL + SQLAlchemy ORM |
| Vector Database | ChromaDB |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| LLM Inference | Groq API — Llama 3.1 8B Instant |
| Authentication | JWT (python-jose) + bcrypt (passlib) |
| PDF Processing | pypdf |
| Text Chunking | LangChain Text Splitters |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Server | Uvicorn (ASGI) |

---

## 🏗️ Architecture


<img width="318" height="186" alt="Architecture diagram" src="https://github.com/user-attachments/assets/bce66235-c785-4818-9786-a98de5a0cef8" />



**RAG Flow:** PDF upload → text extraction → chunking → embedding → ChromaDB storage → on query, semantic search retrieves relevant chunks → chunks + question sent to Llama 3.1 → grounded answer returned.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL (via pgAdmin 4 or CLI)
- A free Groq API key

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-knowledge-hub.git
cd ai-knowledge-hub

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost/ai_knowledge_hub
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_jwt_secret_key_here
```

### Database Setup

```sql
-- Create the database (via pgAdmin 4 or psql)
CREATE DATABASE ai_knowledge_hub;
```

### Run the Server

```bash
python -m uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000` to access the app, or `http://127.0.0.1:8000/docs` for the interactive API documentation.

---

## 📁 Project Structure



<img width="307" height="260" alt="Project structure screenshot" src="https://github.com/user-attachments/assets/3c8e7e8a-efa0-4b00-8d54-801f8037b060" />


---

## 🔑 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Create a new user account |
| POST | `/login` | Authenticate and receive a JWT |
| GET | `/users` | List all registered users |
| GET | `/users/me` | Get current authenticated user |
| POST | `/upload` | Upload and index a PDF document |
| GET | `/documents` | List all indexed documents |
| POST | `/chat` | Send a question to the RAG-powered assistant |
| GET | `/chat/history` | Retrieve conversation history |
| DELETE | `/chat/history` | Clear conversation history |

Full interactive documentation is available at `/docs` (Swagger UI).

---

## 🗺️ Roadmap

- [ ] Document deletion from vector store
- [ ] Full-text search across all documents
- [ ] User profile management (change password/email)
- [ ] Admin panel with usage analytics
- [ ] Persisted chat history per user (database-backed)
- [ ] In-browser PDF preview
- [ ] Redis caching for repeated queries
- [ ] OCR support for scanned documents
- [ ] Docker Compose for one-command deployment
- [ ] CI/CD + cloud deployment (Railway / Render)

---

## 🎯 Skills Demonstrated

LLM Integration · RAG Architecture · Vector Databases · REST API Design · JWT Authentication · Database Modeling (SQLAlchemy) · Semantic Search · Async Python (FastAPI) · Full-Stack Development · Prompt Engineering

---

## 📄 License

This project is open source and available under the MIT License.

---

<div align="center">

Built as a hands-on exploration of production RAG systems — from raw PDF to grounded AI answers.

</div>
