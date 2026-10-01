# Index: AI Knowledge Hub

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-FF6B35)
![Groq](https://img.shields.io/badge/LLM-Groq%20%2B%20Llama%203.1-F55036)
![License](https://img.shields.io/badge/License-MIT-blue)

An AI-powered knowledge management system that lets users upload PDF documents and chat with their content. It applies Retrieval-Augmented Generation (RAG) so every answer is grounded in the retrieved document text, instead of relying on the language model's general knowledge.

**Live demo:** https://ai-knowledge-hub-m0k2.onrender.com

| Demo credentials | |
|---|---|
| Username | `testuser` |
| Password | `Test1234` |

The demo account is provided for demonstration purposes only.

## Overview

Students and researchers often work with several long PDFs and spend a lot of time searching through them for specific information. Index lets them upload their study materials once and ask questions in plain language, getting answers drawn directly from their own documents.

Document search, summarization and question answering live in one workspace, so users do not need to switch between tools.

## Key Features

- **Document-grounded answers.** Responses are generated from content retrieved from the user's uploaded documents.
- **Smart document indexing.** PDFs are extracted, chunked, embedded and stored in a vector database automatically after upload.
- **Semantic search.** Relevant passages are found by meaning using vector similarity, not simple keyword matching.
- **Conversation history.** Chats keep context across questions and can be retrieved or cleared.
- **Quick actions.** One-click shortcuts for common document tasks (see below).
- **Secure authentication.** JWT-based login with Bcrypt password hashing, email validation and password strength checks.
- **Multi-user support.** User registration, role-aware access and an admin-visible user directory.
- **Dashboard.** User and document counts, session query statistics, and health status for the backend, database, model and retrieval system.
- **Responsive interface.** A clean single-page design with document management, chat and analytics views.

## Quick Actions

| Action | Purpose |
|---|---|
| Summarize documents | Produce a concise summary of uploaded material |
| Extract key topics | List the main themes covered |
| Generate report | Create a structured report from the content |
| Suggest questions | Propose study questions based on the material |

## How It Works

1. The user uploads a PDF and the text is extracted with `pypdf`.
2. The text is split into smaller chunks with LangChain Text Splitters.
3. Sentence Transformers (`all-MiniLM-L6-v2`) convert each chunk into a vector, and ChromaDB stores the vectors.
4. A user question is embedded and matched against the stored vectors to find the most relevant chunks.
5. The retrieved chunks and the question are sent to Llama 3.1 through Groq.
6. The interface displays the grounded answer.

## Architecture

```text
GitHub ──► Render ──► FastAPI Backend
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
     PostgreSQL     ChromaDB       Groq API
   (users, chat)   (embeddings)   (Llama 3.1)
```

Authentication, persistence, retrieval and LLM inference are separate responsibilities, which keeps each part easy to maintain and replace.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3.11+, FastAPI, Uvicorn |
| Database | PostgreSQL, SQLAlchemy |
| Retrieval | ChromaDB, Sentence Transformers, pypdf, LangChain Text Splitters |
| Language model | Llama 3.1 8B Instant via Groq API |
| Security | JWT, Bcrypt |
| Hosting | Render |

## Project Structure

```text
AI-Knowledge-Hub/
├── app/
│   ├── main.py        # API routes
│   ├── database.py    # Database connection and session
│   ├── models.py      # SQLAlchemy models
│   ├── schemas.py     # Pydantic schemas
│   ├── auth.py        # JWT and password handling
│   └── rag.py         # RAG pipeline: chunking, indexing, retrieval, prompt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── requirements.txt
├── .env.example
└── README.md
```

The exact structure may vary as the project evolves.

## Getting Started

### Prerequisites

- Python 3.11 or later
- PostgreSQL
- A Groq API key
- Git

### 1. Clone the repository

```bash
git clone https://github.com/swethakannan595-crypto/AI-Knowledge-Hub.git
cd AI-Knowledge-Hub
```

### 2. Set up the environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### 3. Create the database

```sql
CREATE DATABASE ai_knowledge_hub;
```

### 4. Configure environment variables

Create your environment file:

```bash
# macOS / Linux
cp .env.example .env

# Windows
copy .env.example .env
```

Add your settings to `.env` (see [Configuration](#configuration)), then start the server:

```bash
python -m uvicorn app.main:app --reload
```

| Endpoint | URL |
|---|---|
| Application | http://127.0.0.1:8000 |
| Interactive docs | http://127.0.0.1:8000/docs |

## Configuration

The backend reads its settings from `.env` in the project root.

| Variable | Purpose | Example |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:yourpassword@localhost/ai_knowledge_hub` |
| `GROQ_API_KEY` | Groq API key | `your_groq_api_key_here` |
| `SECRET_KEY` | Secret used to sign JWTs | `your_jwt_secret_key_here` |

Never commit `.env` files or API keys. Store secrets in your hosting provider's environment settings.

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/register` | Create a new user account |
| `POST` | `/login` | Authenticate and receive a JWT |
| `GET` | `/users` | List registered users |
| `GET` | `/users/me` | Get the current authenticated user |
| `POST` | `/upload` | Upload and index a PDF |
| `GET` | `/documents` | List indexed documents |
| `POST` | `/chat` | Ask the RAG assistant a question |
| `GET` | `/chat/history` | Retrieve conversation history |
| `DELETE` | `/chat/history` | Clear conversation history |

## Deployment

| Component | Platform | Notes |
|---|---|---|
| Backend | Render | Runs the FastAPI app and holds secrets as environment variables |
| Database | PostgreSQL | Stores users and conversation data |
| Vector store | ChromaDB | Stores document embeddings |
| LLM | Groq API | Serves Llama 3.1 inference |

## Example Questions

- Summarize this document.
- What are the main topics discussed?
- Explain the key concepts.
- What are the important points from this document?
- Generate a report from the document.
- What questions can I prepare from this material?

## Design Principles

- **Grounded by default.** Answers are based on retrieved document content.
- **Semantic retrieval.** Information is found by vector similarity, not keyword matching.
- **Secure by design.** Passwords are hashed, endpoints are protected and secrets live in environment variables.
- **Modular.** Authentication, database, retrieval and LLM responsibilities are kept separate.
- **Simple to use.** Upload a document and start asking questions immediately.

## Screenshots

**AI Chat Interface**

<img width="931" height="432" alt="AI chat interface" src="https://github.com/user-attachments/assets/cdf80dc4-9dbc-48d5-a9b4-6c300eb976a8" />

**Document Index**

<img width="1860" height="872" alt="Document index" src="https://github.com/user-attachments/assets/529611b1-b68c-4c7c-8a33-2c73347e74fe" />

**User Management**

<img width="1868" height="864" alt="User management" src="https://github.com/user-attachments/assets/94a6f6fd-94cc-4080-afd0-b3fb12e1bcd2" />

**Architecture**

<img width="318" height="186" alt="Architecture diagram" src="https://github.com/user-attachments/assets/bce66235-c785-4819-9786-a98de5a0cef8" />

## Roadmap

- Support for additional document formats
- Document deletion from the vector store
- Full-text search across documents
- User profile management
- Advanced admin dashboard
- Persistent chat history per user
- In-browser PDF preview
- Redis caching
- OCR for scanned documents
- Docker Compose setup
- CI/CD pipeline
- Additional cloud deployment options

## Acknowledgements

Built as a hands-on exploration of production-style RAG systems, using FastAPI, PostgreSQL, ChromaDB, Sentence Transformers, LangChain Text Splitters and the Groq API.

## Author

Swetha Kannan
B.Sc. Information Technology
[GitHub](https://github.com/swethakannan595-crypto)

## License

Released under the MIT License. See [LICENSE](LICENSE) for details.
