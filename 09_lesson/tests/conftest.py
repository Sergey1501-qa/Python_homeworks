"""Pytest fixtures for database tests."""
import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Добавляем путь к корню проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импортируем после добавления пути
from config import get_db_url
from models.student import Base, Student


@pytest.fixture
def engine():
    """Create database engine for each test."""
    return create_engine(get_db_url(), echo=False)


@pytest.fixture
def tables(engine):
    """Create all tables for each test."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    """Create database session for each test."""
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_student():
    """Create a sample student for tests."""
    return Student(
        first_name="Иван",
        last_name="Петров",
        email="ivan@example.com",
        birth_date=date(2000, 1, 1),
        grade=10
    )