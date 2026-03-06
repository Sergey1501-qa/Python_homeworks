import requests
from typing import Optional, Dict, Any


class YougileClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()

        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            })

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        try:
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP ошибка {response.status_code}: {response.text}"
            raise Exception(error_msg) from e

    def create_project(self, title: str, users: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/projects"
        payload = {"title": title}

        if users:
            payload["users"] = users

        response = self.session.post(url, json=payload)
        return self._handle_response(response)

    def get_project(self, project_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/projects/{project_id}"
        response = self.session.get(url)
        return self._handle_response(response)

    def update_project(self, project_id: str, title: Optional[str] = None,
                       users: Optional[Dict[str, str]] = None,
                       deleted: Optional[bool] = None) -> Dict[str, Any]:
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

    def delete_project(self, project_id: str) -> Dict[str, Any]:
        return self.update_project(project_id, deleted=True)