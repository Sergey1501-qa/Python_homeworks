"""Негативные тесты для работы с проектами Yougile API"""
import pytest
from api_client import YougileClient


class TestProjectsApiNegative:
    """Негативные тесты для методов работы с проектами"""

    def test_create_project_empty_title(
        self,
        api_client: YougileClient
    ):
        """
        Негативный тест: создание проекта с пустым названием
        Ожидаем ошибку валидации
        """
        with pytest.raises(Exception) as exc_info:
            api_client.create_project(title="")

        error_msg = str(exc_info.value)
        # Разбиваем длинную строку для читаемости
        expected_codes = ["400", "422"]
        assert any(code in error_msg for code in expected_codes), \
            (f"Ожидалась ошибка 400/422, "
             f"получено: {error_msg}")

    def test_create_project_missing_title(
        self,
        api_client: YougileClient
    ):
        """
        Негативный тест: создание проекта без обязательного поля title
        Ожидаем ошибку валидации
        """
        # Пытаемся вызвать метод без title
        with pytest.raises(TypeError):
            api_client.create_project()  # type: ignore

    def test_get_nonexistent_project(
        self,
        api_client: YougileClient
    ):
        """
        Негативный тест: получение несуществующего проекта
        Ожидаем ошибку 404
        """
        nonexistent_id = "00000000-0000-0000-0000-000000000000"

        with pytest.raises(Exception) as exc_info:
            api_client.get_project(nonexistent_id)

        error_msg = str(exc_info.value)
        assert "404" in error_msg, \
            f"Ожидалась ошибка 404, получено: {error_msg}"

    def test_get_project_invalid_id_format(
        self,
        api_client: YougileClient
    ):
        """
        Негативный тест: получение проекта с некорректным форматом ID
        """
        invalid_ids = ["", "123", "abc", "!@#$", " " * 10]

        for invalid_id in invalid_ids:
            with pytest.raises(Exception):
                api_client.get_project(invalid_id)

    def test_update_nonexistent_project(
        self,
        api_client: YougileClient
    ):
        """
        Негативный тест: обновление несуществующего проекта
        Ожидаем ошибку 404
        """
        nonexistent_id = "00000000-0000-0000-0000-000000000000"
        new_title = "Обновление несуществующего"

        with pytest.raises(Exception) as exc_info:
            api_client.update_project(nonexistent_id, title=new_title)

        error_msg = str(exc_info.value)
        assert "404" in error_msg, \
            f"Ожидалась ошибка 404, получено: {error_msg}"

    def test_update_project_without_data(
        self,
        api_client: YougileClient,
        created_project: str
    ):
        """
        Негативный тест: обновление проекта без передачи данных
        Ожидаем ошибку валидации (нужно хотя бы одно поле)
        """
        project_id = created_project

        with pytest.raises(Exception) as exc_info:
            api_client.update_project(project_id)  # Ничего не передаем

        error_msg = str(exc_info.value)
        # Может быть 400 или другое, в зависимости от API
        expected_codes = ["400", "422"]
        assert any(code in error_msg for code in expected_codes), \
            (f"Ожидалась ошибка валидации, "
             f"получено: {error_msg}")

    def test_update_project_empty_title(
        self,
        api_client: YougileClient,
        created_project: str
    ):
        """
        Негативный тест: обновление проекта с пустым названием
        """
        project_id = created_project

        with pytest.raises(Exception) as exc_info:
            api_client.update_project(project_id, title="")

        error_msg = str(exc_info.value)
        expected_codes = ["400", "422"]
        assert any(code in error_msg for code in expected_codes), \
            (f"Ожидалась ошибка валидации, "
             f"получено: {error_msg}")

    def test_unauthorized_access(self):
        """
        Негативный тест: доступ без авторизации
        """
        client = YougileClient(
            "https://yougile.com/api-v2",
            api_key="invalid_key"
        )

        with pytest.raises(Exception) as exc_info:
            client.get_all_projects()

        error_msg = str(exc_info.value)
        expected_codes = ["401", "403"]
        assert any(code in error_msg for code in expected_codes), \
            (f"Ожидалась ошибка авторизации 401/403, "
             f"получено: {error_msg}")

    def test_create_project_with_invalid_users(
        self,
        api_client: YougileClient
    ):
        """
        Негативный тест: создание проекта с некорректными правами
        """
        project_title = "Проект с неверными правами"
        invalid_users = {
            "invalid-user-id": "invalid_role"  # Несуществующая роль
        }

        with pytest.raises(Exception) as exc_info:
            api_client.create_project(
                title=project_title,
                users=invalid_users
            )

        error_msg = str(exc_info.value)
        expected_codes = ["400", "422"]
        assert any(code in error_msg for code in expected_codes), \
            (f"Ожидалась ошибка валидации, "
             f"получено: {error_msg}")

    def test_rate_limit_exceeded(
        self,
        api_client: YougileClient
    ):
        """
        Негативный тест: превышение лимита запросов
        Yougile ограничивает 50 запросов в минуту
        """
        # Делаем много быстрых запросов
        with pytest.raises(Exception) as exc_info:
            for i in range(60):  # Пытаемся сделать 60 запросов
                api_client.get_all_projects(limit=1)

        error_msg = str(exc_info.value)
        # Может быть 429 Too Many Requests
        expected_patterns = ["429", "Too Many Requests"]
        assert any(pattern in error_msg for pattern in expected_patterns), \
            (f"Ожидалась ошибка 429, "
             f"получено: {error_msg}")
