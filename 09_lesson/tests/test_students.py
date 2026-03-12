"""Tests for Student model and database operations."""
import pytest
from datetime import date
from sqlalchemy.exc import IntegrityError
from models.student import Student


class TestStudentModel:
    """Test cases for Student model."""

    def test_create_student(self, db_session):
        """Test creating a new student."""
        # Создаем студента
        student = Student(
            first_name="Иван",
            last_name="Петров",
            email="ivan@example.com",
            birth_date=date(2000, 1, 1),
            grade=10
        )
        db_session.add(student)
        db_session.commit()

        # Проверяем
        assert student.id is not None
        assert student.first_name == "Иван"
        assert student.last_name == "Петров"
        assert student.email == "ivan@example.com"
        assert student.birth_date == date(2000, 1, 1)
        assert student.grade == 10

    def test_read_student(self, db_session):
        """Test reading a student from database."""
        # Создаем студента
        student = Student(
            first_name="Петр",
            last_name="Сидоров",
            email="petr@example.com",
            birth_date=date(2001, 2, 2),
            grade=9
        )
        db_session.add(student)
        db_session.commit()

        # Читаем студента
        found = db_session.query(Student).filter_by(email="petr@example.com").first()
        assert found is not None
        assert found.first_name == "Петр"
        assert found.last_name == "Сидоров"

    def test_update_student(self, db_session):
        """Test updating a student."""
        # Создаем студента
        student = Student(
            first_name="Мария",
            last_name="Иванова",
            email="maria@example.com",
            birth_date=date(2002, 3, 3),
            grade=8
        )
        db_session.add(student)
        db_session.commit()

        # Обновляем
        student.grade = 9
        db_session.commit()

        # Проверяем
        updated = db_session.query(Student).filter_by(email="maria@example.com").first()
        assert updated.grade == 9

    def test_delete_student(self, db_session):
        """Test deleting a student."""
        # Создаем студента
        student = Student(
            first_name="Анна",
            last_name="Смирнова",
            email="anna@example.com",
            birth_date=date(2003, 4, 4),
            grade=7
        )
        db_session.add(student)
        db_session.commit()
        student_id = student.id

        # Удаляем
        db_session.delete(student)
        db_session.commit()

        # Проверяем
        deleted = db_session.query(Student).filter_by(id=student_id).first()
        assert deleted is None

    def test_unique_email_constraint(self, db_session):
        """Test that email must be unique."""
        # Создаем первого студента
        student1 = Student(
            first_name="Ольга",
            last_name="Козлова",
            email="olga@example.com",
            birth_date=date(2004, 5, 5),
            grade=6
        )
        db_session.add(student1)
        db_session.commit()

        # Пытаемся создать второго с тем же email
        student2 = Student(
            first_name="Дмитрий",
            last_name="Новиков",
            email="olga@example.com",  # Тот же email
            birth_date=date(2005, 6, 6),
            grade=5
        )
        db_session.add(student2)
        with pytest.raises(IntegrityError):
            db_session.commit()
        db_session.rollback()

    def test_filter_by_grade(self, db_session):
        """Test filtering students by grade."""
        # Создаем нескольких студентов
        students = [
            Student(
                first_name="Алексей",
                last_name="Алексеев",
                email="aleksey1@example.com",
                birth_date=date(2000, 1, 1),
                grade=10
            ),
            Student(
                first_name="Алексей",
                last_name="Петров",
                email="aleksey2@example.com",
                birth_date=date(2001, 2, 2),
                grade=10
            ),
            Student(
                first_name="Борис",
                last_name="Борисов",
                email="boris@example.com",
                birth_date=date(2002, 3, 3),
                grade=9
            ),
        ]
        for student in students:
            db_session.add(student)
        db_session.commit()

        # Фильтруем по классу 10
        tenth_grade = db_session.query(Student).filter(Student.grade == 10).all()
        assert len(tenth_grade) == 2

        # Фильтруем по классу 9
        ninth_grade = db_session.query(Student).filter(Student.grade == 9).all()
        assert len(ninth_grade) == 1
