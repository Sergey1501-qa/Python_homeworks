"""
Модель Student для SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import date

Base = declarative_base()


class Student(Base):
    """Модель студента"""
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    birth_date = Column(Date, nullable=False)
    group_name = Column(String(20), nullable=False)
    enrollment_year = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.first_name} {self.last_name}')>"

    def to_dict(self):
        """Преобразует объект в словарь"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'group_name': self.group_name,
            'enrollment_year': self.enrollment_year
        }