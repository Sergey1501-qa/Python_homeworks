"""
Тесты для CRUD операций со студентами
"""
import pytest
from datetime import date, timedelta
from sqlalchemy.exc import IntegrityError

from models.student import Student


class TestStudentCRUD:
    """Тесты для CRUD операций со студентами"""

    # ========== Тест на добавление (CREATE) ==========

    def test_create_student(self, db_session, test_student_data):
        """
        Тест 1: добавление нового студента в базу данных

        Шаги:
        1. Создать объект студента
        2. Добавить в сессию
        3. Сохранить в БД
        4. Проверить, что студент появился в БД
        5. Удалить тестовые данные
        """
        # 1-2. Создаем и добавляем студента
        student = Student(**test_student_data)
        db_session.add(student)
        db_session.commit()

        # 3. Получаем ID сохраненного студента
        student_id = student.id

        try:
            # 4. Проверяем, что студент сохранился
            saved_student = db_session.query(Student).filter(
                Student.id == student_id
            ).first()

            assert saved_student is not None, "Студент не найден в БД"
            assert saved_student.first_name == test_student_data['first_name']
            assert saved_student.last_name == test_student_data['last_name']
            assert saved_student.email == test_student_data['email']
            assert saved_student.birth_date == test_student_data['birth_date']
            assert saved_student.group_name == test_student_data['group_name']
            assert saved_student.enrollment_year == test_student_data['enrollment_year']

            print(f"\n✅ Студент успешно создан с ID: {student_id}")

        finally:
            # 5. Удаляем тестовые данные
            db_session.delete(student)
            db_session.commit()
            print(f"🧹 Тестовые данные удалены")

    # ========== Тест на изменение (UPDATE) ==========

    def test_update_student(self, db_session, created_student):
        """
        Тест 2: изменение данных существующего студента

        Шаги:
        1. Получить студента из БД
        2. Изменить его данные
        3. Сохранить изменения
        4. Проверить, что данные обновились
        """
        # 1. Получаем студента
        student = db_session.query(Student).filter(
            Student.id == created_student
        ).first()

        # 2. Изменяем данные
        new_last_name = "Иванов"
        new_group = "ГР-789"

        old_last_name = student.last_name
        old_group = student.group_name

        student.last_name = new_last_name
        student.group_name = new_group

        # 3. Сохраняем изменения
        db_session.commit()
        print(f"\n✏️ Обновление: {old_last_name} -> {new_last_name}, {old_group} -> {new_group}")

        # 4. Проверяем, что данные обновились
        updated_student = db_session.query(Student).filter(
            Student.id == created_student
        ).first()

        assert updated_student.last_name == new_last_name, \
            "Фамилия не обновилась"
        assert updated_student.group_name == new_group, \
            "Группа не обновилась"
        assert updated_student.first_name != new_last_name, \
            "Имя не должно измениться"

        print(f"✅ Данные студента {created_student} успешно обновлены")

    # ========== Тест на удаление (DELETE) ==========

    def test_delete_student(self, db_session, created_student):
        """
        Тест 3: удаление студента из базы данных

        Шаги:
        1. Проверить, что студент существует в БД
        2. Удалить студента
        3. Проверить, что студент больше не существует в БД
        """
        # 1. Проверяем, что студент существует
        student = db_session.query(Student).filter(
            Student.id == created_student
        ).first()
        assert student is not None, "Студент должен существовать до удаления"
        print(f"\n🔍 Найден студент с ID: {created_student}")

        # 2. Удаляем студента
        db_session.delete(student)
        db_session.commit()
        print(f"🗑️ Студент {created_student} удален")

        # 3. Проверяем, что студент удален
        deleted_student = db_session.query(Student).filter(
            Student.id == created_student
        ).first()

        assert deleted_student is None, "Студент не был удален"
        print(f"✅ Подтверждено: студент {created_student} больше не существует в БД")