"""Фикстуры pytest для тестов Yougile API"""
import pytest
import sys
import os
from typing import Generator, Dict, Any

# Добавляем путь к проекту для импортов
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from api_client import YougileClient
from utils.data_generator import generate_unique_title

# Импортируем конфигурацию
try:
    from config import YOUGILE_CONFIG
except ImportError:
    YOUGILE_CONFIG = {
        "base_url": "https://yougile.com/api-v2",
        "auth": {}
    }


@pytest.fixture(scope="session")
def api_client() -> YougileClient:
    """
    Фикстура для создания клиента API

    Returns:
        YougileClient: Настроенный клиент для работы с API
    """
    config = YOUGILE_CONFIG
    base_url = config["base_url"]

    # Если есть готовый API ключ, используем его
    if config["auth"].get("api_key"):
        client = YougileClient(base_url, config["auth"]["api_key"])
    # Иначе пытаемся получить ключ по логину/паролю
    elif (config["auth"].get("login") and
          config["auth"].get("password") and
          config["auth"].get("company_id")):
        client = YougileClient(base_url)
        client.get_api_key_by_credentials(
            config["auth"]["login"],
            config["auth"]["password"],
            config["auth"]["company_id"]
        )
    else:
        pytest.skip("Не указаны данные для авторизации. Заполните config.py")

    return client


@pytest.fixture
def test_project_data() -> Dict[str, Any]:
    """
    Фикстура с данными для тестового проекта

    Returns:
        Dict: Данные проекта
    """
    return {
        "title": generate_unique_title("API Тест"),
        "users": {}  # Пустой словарь прав
    }


@pytest.fixture
def created_project(
        api_client: YougileClient,
        test_project_data: Dict[str, Any]
) -> Generator[str, None, None]:
    """
    Фикстура создает проект и удаляет его после теста

    Args:
        api_client: Клиент API
        test_project_data: Данные проекта

    Yields:
        str: ID созданного проекта
    """
    # Создаем проект
    response = api_client.create_project(
        title=test_project_data["title"],
        users=test_project_data["users"]
    )

    project_id = response.get("id")
    if not project_id:
        pytest.fail("Не удалось создать проект для теста")

    yield project_id

    # Очистка: помечаем проект как удаленный
    try:
        api_client.delete_project(project_id)
    except Exception:
        print(f"Не удалось удалить проект {project_id}")
