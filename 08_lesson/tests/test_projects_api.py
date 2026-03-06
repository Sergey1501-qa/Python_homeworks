import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_generator import generate_unique_title


class TestProjectsApiPositive:
    """Позитивные тесты"""
    
    def test_create_project_minimal(self, api_client):
        """Создание проекта с минимальными данными"""
        title = generate_unique_title("Минимальный")
        
        response = api_client.create_project(title=title)
        
        assert response is not None
        assert "id" in response
        project_id = response["id"]
        
        # Очистка
        api_client.delete_project(project_id)
    
    def test_get_project_by_id(self, api_client, created_project):
        """Получение проекта по ID"""
        project_id = created_project
        
        response = api_client.get_project(project_id)
        
        assert response is not None
        assert response["id"] == project_id
        assert "title" in response
    
    def test_update_project_title(self, api_client, created_project):
        """Обновление названия проекта"""
        project_id = created_project
        new_title = generate_unique_title("Обновленный")
        
        update_response = api_client.update_project(project_id, title=new_title)
        assert update_response is not None
        
        get_response = api_client.get_project(project_id)
        assert get_response["title"] == new_title
    
    def test_update_project_deleted_flag(self, api_client, created_project):
        """Мягкое удаление проекта"""
        project_id = created_project
        
        response = api_client.update_project(project_id, deleted=True)
        assert response is not None
        
        get_response = api_client.get_project(project_id)
        assert get_response["deleted"] is True