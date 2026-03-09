"""
Фикстуры pytest для тестирования БД
"""
import pytest
import os
import sys
from datetime import date, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Добавляем путь к проекту
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from models.student import Base, Student
from config import get_db_url

# Получаем строку подключения
DATABASE_URL = get_db_url()


@pytest.fixture(scope="session")
def engine():
    """Фикстура для создания движка базы данных"""
    _engine = create_engine(DATABASE_URL, echo=True)

    # Создаем таблицы, если их нет
    Base.metadata.create_all(_engine)

    yield _engine

    # Очистка после всех тестов (опционально)
    # Base.metadata.drop_all(_engine)


@pytest.fixture(scope="function")
def db_session(engine):
    """Фикстура для создания сессии базы данных"""
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # Откатываем все незакоммиченные изменения
    session.rollback()
    # Закрываем сессию
    session.close()


@pytest.fixture
def test_student_data():
    """Фикстура с тестовыми данными студента"""
    from datetime import date
    import random

    # Генерируем уникальный email
    unique_id = random.randint(1000, 9999)
    return {
        'first_name': 'Иван',
        'last_name': 'Петров',
        'email': f'ivan.petrov_{unique_id}@example.com',
        'birth_date': date(2000, 5, 15),
        'group_name': 'АБ-123',
        'enrollment_year': 2023
    }


@pytest.fixture
def created_student(db_session, test_student_data):
    """
    Фикстура создает студента и удаляет его после теста
    """
    # Создаем студента
    student = Student(**test_student_data)
    db_session.add(student)
    db_session.commit()

    # Сохраняем ID для использования в тесте
    student_id = student.id

    yield student_id

    # Удаляем созданного студента после теста
    db_session.query(Student).filter(Student.id == student_id).delete()
    db_session.commit()