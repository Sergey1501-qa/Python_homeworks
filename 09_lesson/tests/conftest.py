"""Pytest fixtures for database tests."""
import pytest
import os
import sys
import importlib.util
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Добавляем путь к корню проекта
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Загружаем config.py напрямую по пути
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config.py'))
spec = importlib.util.spec_from_file_location("project_config", config_path)
config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config_module)

DATABASE_URL = config_module.get_db_url()

# Импортируем модели (теперь путь должен работать)
from models.student import Base, Student


@pytest.fixture(scope="session")
def engine():
    """Create database engine for tests."""
    return create_engine(DATABASE_URL, echo=False)


@pytest.fixture(scope="function")
def tables(engine):
    """Create all tables for each test."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(engine, tables):
    """Create database session for each test."""
    TestingSessionLocal = sessionmaker(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_student_data():
    """Provide sample student data for tests."""
    return {
        "first_name": "Иван",
        "last_name": "Петров",
        "email": "ivan@example.com",
        "birth_date": date(2000, 1, 1),
        "grade": 10
    }