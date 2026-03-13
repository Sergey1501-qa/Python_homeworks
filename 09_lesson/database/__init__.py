"""Database package initialization."""
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Добавляем путь к корню проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import get_db_url

# Создаем engine и session
engine = create_engine(get_db_url())
SessionLocal = sessionmaker(bind=engine)


def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()