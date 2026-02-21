import pytest
from selenium import webdriver
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def calculator_page(driver):
    from pages.calculator_page import CalculatorPage
    return CalculatorPage(driver)