from app.db.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    try:
        conn.execute(text("ALTER TABLE documents ADD COLUMN chroma_ids TEXT DEFAULT ''"))
        conn.commit()
        print("Column added successfully!")
    except Exception as e:
        print(f"Add column error (may already exist): {e}")

with engine.connect() as conn:
    result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='documents'"))
    print("\nCurrent columns in 'documents' table:")
    for row in result:
        print("-", row[0])