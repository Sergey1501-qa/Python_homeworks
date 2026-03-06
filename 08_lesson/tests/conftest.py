import pytest
import sys
import os

# Добавляем путь к корневой папке проекта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api_client import YougileClient
from tests.config import YOUGILE_CONFIG


@pytest.fixture
def api_client():
    """Фикстура для создания клиента API"""
    base_url = YOUGILE_CONFIG["base_url"]
    api_key = YOUGILE_CONFIG["api_key"]

    if not api_key or api_key == "ВАШ_API_КЛЮЧ_ЗДЕСЬ":
        pytest.skip("Не указан API ключ. Заполните tests/config.py")

    return YougileClient(base_url, api_key)


@pytest.fixture
def created_project(api_client):
    """Фикстура создает проект и возвращает его ID"""
    from utils.data_generator import generate_unique_title

    title = generate_unique_title("Фикстура")
    response = api_client.create_project(title=title)
    project_id = response.get("id")

    yield project_id

    # Очистка после теста
    try:
        api_client.delete_project(project_id)
    except:
        pass