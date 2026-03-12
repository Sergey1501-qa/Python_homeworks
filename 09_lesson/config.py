"""Конфигурационный файл для подключения к базе данных."""
import os


def get_db_url() -> str:
    """
    Возвращает URL для подключения к базе данных.

    Returns:
        str: URL базы данных
    """
    return os.getenv(
        'DATABASE_URL',
        'sqlite:///./test.db'
    )