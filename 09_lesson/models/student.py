"""Student model for database."""
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Student(Base):
    """Student model representing students table."""

    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    birth_date = Column(Date, nullable=False)
    grade = Column(Integer, nullable=False)

    def __repr__(self) -> str:
        """String representation of Student."""
        return (
            f"<Student(id={self.id}, "
            f"name='{self.first_name} {self.last_name}', "
            f"email='{self.email}')>"
        )
