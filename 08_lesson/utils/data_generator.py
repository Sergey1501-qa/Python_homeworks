from datetime import datetime
import random
import string


def generate_unique_title(prefix: str = "Тестовый проект") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"{prefix}_{timestamp}_{random_suffix}"