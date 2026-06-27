from app.db.database import engine
from app.models.document import Document
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS documents CASCADE"))
    conn.commit()
    print("Old documents table dropped.")

Document.__table__.create(bind=engine)
print("New documents table created.")
