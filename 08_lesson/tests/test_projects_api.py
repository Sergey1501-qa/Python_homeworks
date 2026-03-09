"""Позитивные тесты для работы с проектами Yougile API"""
from api_client import YougileClient
from utils.data_generator import generate_unique_title


class TestProjectsApiPositive:
    """Позитивные тесты для методов работы с проектами"""

    def test_create_project_minimal(
        self,
        api_client: YougileClient
    ):
        """
        Позитивный тест: создание проекта с минимальными данными
        Метод: [POST] /api-v2/projects
        """
        # Данные для теста
        project_title = generate_unique_title("Минимальный проект")

        # Выполняем запрос
        response = api_client.create_project(title=project_title)

        # Проверяем ответ
        assert response is not None, "Ответ не должен быть пустым"
        assert "id" in response, \
            "В ответе должен быть ID созданного проекта"

        project_id = response["id"]
        assert project_id, "ID проекта не должен быть пустым"

        # Проверяем, что проект действительно создан
        get_response = api_client.get_project(project_id)
        assert get_response["title"] == project_title, \
            "Название проекта не совпадает"

        # Очистка
        api_client.delete_project(project_id)

    def test_create_project_full(
        self,
        api_client: YougileClient
    ):
        """
        Позитивный тест: создание проекта с полными данными
        Метод: [POST] /api-v2/projects
        """
        # Данные для теста
        project_title = generate_unique_title("Полный проект")

        # Выполняем запрос
        response = api_client.create_project(title=project_title)

        # Проверяем ответ
        assert response is not None
        assert "id" in response

        project_id = response["id"]

        # Проверяем созданный проект
        get_response = api_client.get_project(project_id)
        assert get_response["id"] == project_id
        assert get_response["title"] == project_title
        assert "users" in get_response

        # Очистка
        api_client.delete_project(project_id)

    def test_get_project_by_id(
        self,
        api_client: YougileClient,
        created_project: str
    ):
        """
        Позитивный тест: получение проекта по ID
        Метод: [GET] /api-v2/projects/{id}
        """
        project_id = created_project

        # Выполняем запрос
        response = api_client.get_project(project_id)

        # Проверяем ответ
        assert response is not None
        assert response["id"] == project_id, "ID проекта не совпадает"
        assert "title" in response, "В ответе должно быть название"
        assert "users" in response, \
            "В ответе должны быть права пользователей"
        assert "deleted" in response, \
            "В ответе должен быть флаг удаления"

    def test_update_project_title(
        self,
        api_client: YougileClient,
        created_project: str
    ):
        """
        Позитивный тест: обновление названия проекта
        Метод: [PUT] /api-v2/projects/{id}
        """
        project_id = created_project
        new_title = generate_unique_title("Обновленный проект")

        # Выполняем запрос на обновление
        update_response = api_client.update_project(
            project_id,
            title=new_title
        )

        # Проверяем ответ обновления
        assert update_response is not None

        # Проверяем, что название действительно обновилось
        get_response = api_client.get_project(project_id)
        assert get_response["title"] == new_title, \
            "Название проекта не обновилось"

    def test_update_project_deleted_flag(
        self,
        api_client: YougileClient,
        created_project: str
    ):
        """
        Позитивный тест: мягкое удаление проекта
        Метод: [PUT] /api-v2/projects/{id}
        """
        project_id = created_project

        # Помечаем проект как удаленный
        update_response = api_client.update_project(
            project_id,
            deleted=True
        )

        # Проверяем ответ
        assert update_response is not None

        # Проверяем, что проект помечен как удаленный
        get_response = api_client.get_project(project_id)
        assert get_response["deleted"] is True, \
            "Проект не помечен как удаленный"

    def test_create_and_get_multiple_projects(
        self,
        api_client: YougileClient
    ):
        """
        Позитивный тест: создание нескольких проектов
        и получение списка
        """
        created_ids = []

        try:
            # Создаем 3 проекта
            for i in range(3):
                title = generate_unique_title(f"Проект {i+1}")
                response = api_client.create_project(title=title)
                created_ids.append(response["id"])

            # Получаем список всех проектов
            all_projects = api_client.get_all_projects(limit=100)

            assert "content" in all_projects
            assert len(all_projects["content"]) > 0

            # Проверяем, что наши проекты есть в списке
            project_ids = [p["id"] for p in all_projects["content"]]
            for created_id in created_ids:
                assert created_id in project_ids, \
                    f"Проект {created_id} не найден в списке"

        finally:
            # Очистка
            for project_id in created_ids:
                try:
                    api_client.delete_project(project_id)
                except Exception:
                    pass
