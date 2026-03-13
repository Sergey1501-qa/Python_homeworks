"""
Пример файла конфигурации.
Скопируйте этот файл как config.py и заполните своими данными.
"""

# Конфигурация подключения к базе данных
DB_CONFIG = {
    "username": "postgres",  # Замените на ваше имя пользователя
    "password": "123",  # Замените на ваш пароль
    "host": "localhost",
    "port": 5432,
    "database": "mydatabase"  # Замените на название вашей БД
}

# Строка подключения формируется автоматически
def get_db_url():
    """Возвращает строку подключения к базе данных"""
    return (f"postgresql://{DB_CONFIG['username']}:{DB_CONFIG['password']}"
            f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")