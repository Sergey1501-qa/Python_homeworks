import pytest
import uuid
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestProjectsApiNegative:
    """Негативные тесты"""

    def test_create_project_empty_title(self, api_client):
        """Создание проекта с пустым названием"""
        with pytest.raises(Exception) as exc_info:
            api_client.create_project(title="")

        error_msg = str(exc_info.value)
        assert "400" in error_msg or "422" in error_msg

    def test_get_nonexistent_project(self, api_client):
        """Получение несуществующего проекта"""
        nonexistent_id = str(uuid.uuid4())

        with pytest.raises(Exception) as exc_info:
            api_client.get_project(nonexistent_id)

        error_msg = str(exc_info.value)
        assert "404" in error_msg

    def test_update_nonexistent_project(self, api_client):
        """Обновление несуществующего проекта"""
        nonexistent_id = str(uuid.uuid4())

        with pytest.raises(Exception) as exc_info:
            api_client.update_project(nonexistent_id, title="Новое название")

        error_msg = str(exc_info.value)
        assert "404" in error_msg