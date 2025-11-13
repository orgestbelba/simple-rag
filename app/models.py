from sqlalchemy import Column, String, Text, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

Base = declarative_base()

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String(50))  # "wikipedia", "medium", "reddit"
    title = Column(String(500))
    url = Column(String(2048), unique=True)
    content = Column(Text)  # First 2000 chars
    author = Column(String(255), nullable=True)
    scraped_at = Column(DateTime, default=datetime.utcnow)

# DB Setup
engine = create_engine("sqlite:///articles.db", connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()