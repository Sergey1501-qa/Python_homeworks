import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    """Фикстура для создания драйвера"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()