import random
import string
from datetime import datetime


def generate_unique_title(prefix: str = "Тестовый проект") -> str:
    """
    Генерирует уникальное название для проекта

    Args:
        prefix: Префикс названия

    Returns:
        str: Уникальное название с временной меткой
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = ''.join(
        random.choices(string.ascii_letters + string.digits, k=6)
    )
    return f"{prefix}_{timestamp}_{random_suffix}"


def generate_random_string(length: int = 10) -> str:
    """
    Генерирует случайную строку

    Args:
        length: Длина строки

    Returns:
        str: Случайная строка
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
