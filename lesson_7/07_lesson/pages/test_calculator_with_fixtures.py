import sys
import os
import pytest
from selenium import webdriver
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.calculator_page import CalculatorPage


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def calculator_page(driver):
    return CalculatorPage(driver)


def test_calculator_with_fixtures(calculator_page):
    calculator_page.open()
    calculator_page.set_delay(45)
    calculator_page.click_button("7")
    calculator_page.click_button("+")
    calculator_page.click_button("8")
    calculator_page.click_button("=")
    calculator_page.wait_for_result("15")

    result = calculator_page.get_result()
    assert result == "15", f"Ожидался результат '15', но получено '{result}'"