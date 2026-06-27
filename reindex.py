import chromadb
import os
from app.db.database import SessionLocal
from app.models.document import Document
from app.services.rag import add_document

print('Step 1: Clearing ChromaDB...')
try:
    client = chromadb.PersistentClient(path='app/chroma_db')
    client.delete_collection('documents')
    print('  Collection deleted')
except Exception as e:
    print(f'  Note: {e}')

print('Step 2: Re-indexing all documents...')
db = SessionLocal()
docs = db.query(Document).all()
print(f'  Found {len(docs)} documents')
for doc in docs:
    if os.path.exists(doc.file_path):
        print(f'  Indexing: {doc.filename}')
        result = add_document(doc.file_path, doc.filename)
        print('  Result: OK' if result else '  Result: FAILED')
    else:
        print(f'  SKIPPED - missing: {doc.file_path}')
db.close()

print('Step 3: Verifying...')
from app.services.rag import get_all_documents
indexed = get_all_documents()
for name in indexed:
    print(f'  - {name}')
print(f'Done! {len(indexed)} documents indexed')