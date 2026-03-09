# Домашнее задание: Тестирование БД с SQLAlchemy

## Структура проекта

- `models/` - модели SQLAlchemy
- `tests/` - тесты
- `config.py` - конфигурация подключения к БД
- `requirements.txt` - зависимости

## Тесты

### Основные тесты (3 штуки):
1. `test_create_student` - добавление студента
2. `test_update_student` - изменение данных студента
3. `test_delete_student` - удаление студента

### Дополнительные тесты:
- `test_create_student_duplicate_email` - негативный тест на уникальность
- `test_get_student_by_id` - получение по ID
- `test_update_nonexistent_student` - обновление несуществующего
- `test_get_all_students` - получение всех записей

## Запуск тестов

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск всех тестов
pytest tests/ -v

# Запуск с подробным выводом
pytest tests/test_students.py -v -s

# Запуск конкретного теста
pytest tests/test_students.py::TestStudentCRUD::test_create_student -v