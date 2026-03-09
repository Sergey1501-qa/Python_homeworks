"""Клиент для работы с Yougile API"""
import requests
from typing import Optional, Dict, Any


class YougileClient:
    """Клиент для взаимодействия с Yougile REST API v2"""

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Инициализация клиента

        Args:
            base_url: Базовый URL API (например, https://yougile.com/api-v2)
            api_key: API ключ для авторизации
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()

        # Если есть ключ, добавляем заголовок авторизации
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            })

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        Обрабатывает ответ от API

        Args:
            response: Объект ответа requests

        Returns:
            Dict: JSON ответа

        Raises:
            Exception: При ошибке запроса
        """
        try:
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP ошибка {response.status_code}: {response.text}"
            raise Exception(error_msg) from e
        except Exception as e:
            raise Exception(f"Ошибка при обработке ответа: {e}") from e

    def get_api_key_by_credentials(
            self,
            login: str,
            password: str,
            company_id: str
    ) -> str:
        """
        Получает API ключ по логину/паролю

        Args:
            login: Email пользователя
            password: Пароль
            company_id: ID компании

        Returns:
            str: API ключ
        """
        url = f"{self.base_url}/auth/keys"
        payload = {
            "login": login,
            "password": password,
            "companyId": company_id
        }

        response = self.session.post(url, json=payload)
        result = self._handle_response(response)

        if "key" not in result:
            raise Exception("Не удалось получить API ключ")

        self.api_key = result["key"]
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

        return self.api_key

    # ========== Методы для работы с проектами ==========

    def create_project(
            self,
            title: str,
            users: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Создает новый проект

        [POST] /api-v2/projects

        Args:
            title: Название проекта (обязательно)
            users: Словарь с правами пользователей
                  {user_id: "admin"/"user"/"guest"}

        Returns:
            Dict: Ответ API с ID созданного проекта
        """
        url = f"{self.base_url}/projects"
        payload = {"title": title}

        if users:
            payload["users"] = users

        response = self.session.post(url, json=payload)
        return self._handle_response(response)

    def get_project(self, project_id: str) -> Dict[str, Any]:
        """
        Получает информацию о проекте по ID

        [GET] /api-v2/projects/{id}

        Args:
            project_id: ID проекта

        Returns:
            Dict: Информация о проекте
        """
        url = f"{self.base_url}/projects/{project_id}"
        response = self.session.get(url)
        return self._handle_response(response)

    def update_project(
            self,
            project_id: str,
            title: Optional[str] = None,
            users: Optional[Dict[str, str]] = None,
            deleted: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Обновляет существующий проект

        [PUT] /api-v2/projects/{id}

        Args:
            project_id: ID проекта
            title: Новое название проекта
            users: Обновленные права пользователей
            deleted: Пометить проект как удаленный

        Returns:
            Dict: Ответ API
        """
        url = f"{self.base_url}/projects/{project_id}"
        payload = {}

        if title is not None:
            payload["title"] = title
        if users is not None:
            payload["users"] = users
        if deleted is not None:
            payload["deleted"] = deleted

        response = self.session.put(url, json=payload)
        return self._handle_response(response)

    def get_all_projects(
            self,
            limit: int = 100,
            offset: int = 0
    ) -> Dict[str, Any]:
        """
        Получает список всех проектов

        [GET] /api-v2/projects

        Args:
            limit: Количество записей
            offset: Смещение

        Returns:
            Dict: Список проектов
        """
        url = f"{self.base_url}/projects"
        params = {"limit": limit, "offset": offset}
        response = self.session.get(url, params=params)
        return self._handle_response(response)

    def delete_project(self, project_id: str) -> Dict[str, Any]:
        """
        Помечает проект как удаленный (мягкое удаление)

        Args:
            project_id: ID проекта

        Returns:
            Dict: Ответ API
        """
        return self.update_project(project_id, deleted=True)
