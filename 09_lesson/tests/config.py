"""
Конфигурация для подключения к базе данных PostgreSQL
"""

# Конфигурация подключения к базе данных
DB_CONFIG = {
    "username": "postgres",      # ваш пользователь
    "password": "123",          # ваш пароль
    "host": "localhost",
    "port": 5432,
    "database": "QA"              # название вашей БД
}

def get_db_url():
    """Возвращает строку подключения к базе данных"""
    return (f"postgresql://{DB_CONFIG['username']}:{DB_CONFIG['password']}"
            f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")