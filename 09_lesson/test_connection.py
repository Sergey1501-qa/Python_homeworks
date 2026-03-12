"""Тест подключения к базе данных."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import get_db_url, DB_CONFIG
from sqlalchemy import create_engine, text


def test_connection():
    """Проверяет подключение к базе данных."""
    print("Параметры подключения:")
    print(f"  Хост: {DB_CONFIG['host']}")
    print(f"  Порт: {DB_CONFIG['port']}")
    print(f"  База: {DB_CONFIG['database']}")
    print(f"  Пользователь: {DB_CONFIG['username']}")

    db_url = get_db_url()
    print(f"\nURL подключения: {db_url}")

    # Пробуем подключиться
    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"\n✅ Подключение успешно!")
            print(f"Версия PostgreSQL: {version}")
        return True
    except Exception as e:
        print(f"\n❌ Ошибка подключения: {e}")
        return False


if __name__ == "__main__":
    test_connection()