# Тестирование Yougile API

## Описание

Автотесты для методов работы с проектами Yougile API v2:
- `POST /api-v2/projects` - создание проекта
- `GET /api-v2/projects/{id}` - получение проекта
- `PUT /api-v2/projects/{id}` - обновление проекта

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate  # для Linux/Mac
   venv\Scripts\activate     # для Windows