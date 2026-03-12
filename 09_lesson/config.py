"""Конфигурационный файл для подключения к базе данных."""
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла если он есть
load_dotenv()


def get_db_url() -> str:
    """
    Возвращает URL для подключения к базе данных PostgreSQL.

    Returns:
        str: URL для подключения к PostgreSQL
    """
    # Ваши данные из команды:
    username = os.getenv('DB_USERNAME', 'postgres')      # пользователь postgres
    password = os.getenv('DB_PASSWORD', '123')              # нужно вставить ваш пароль
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    database = os.getenv('DB_NAME', 'QA')                # база данных QA

    return f"postgresql://{username}:{password}@{host}:{port}/{database}"


# Для удобства
DB_CONFIG = {
    "username": 'postgres',
    "password": '123',
    "host": 'localhost',
    "port": 5432,
    "database": 'QA'
}