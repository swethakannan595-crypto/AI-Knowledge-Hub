import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
import os
import uuid

CHROMA_DIR = "app/chroma_db"

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

_client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = _client.get_or_create_collection(
    name="documents",
    embedding_function=embedding_fn
)


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def add_document_to_vectorstore(file_path: str, filename: str = None) -> list[str]:
    text = extract_text_from_pdf(file_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_text(text)

    if not chunks:
        return []

    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"filename": filename or os.path.basename(file_path)} for _ in chunks]

    collection.add(documents=chunks, ids=ids, metadatas=metadatas)
    return ids


def delete_document_from_vectorstore(chroma_ids: list[str]):
    if not chroma_ids:
        return
    collection.delete(ids=chroma_ids)


def search_documents(query: str, k: int = 4) -> list[str]:
    results = collection.query(query_texts=[query], n_results=k)
    docs = results.get("documents")
    if not docs or not docs[0]:
        return []
    return docs[0]