from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.db.database import Base


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
