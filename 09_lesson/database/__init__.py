"""Database package initialization."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
