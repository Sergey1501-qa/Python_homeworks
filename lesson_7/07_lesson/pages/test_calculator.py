import sys
import os
import pytest
from selenium import webdriver
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.calculator_page import CalculatorPage, CalculatorPageDetailed


class TestCalculator:

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.calculator_page = CalculatorPage(self.driver)

    def teardown_method(self):
        """Очистка после каждого теста"""
        self.driver.quit()

    def test_calculator_with_45_second_delay(self):
        """
        Тест проверяет работу калькулятора с задержкой 45 секунд.
        """
        # Шаг 1: Открываем страницу калькулятора
        self.calculator_page.open()

        # Шаг 2: Устанавливаем задержку 45 секунд
        self.calculator_page.set_delay(45)

        # Шаг 3: Выполняем вычисление 7 + 8
        self.calculator_page.click_button("7")
        self.calculator_page.click_button("+")
        self.calculator_page.click_button("8")
        self.calculator_page.click_button("=")

        # Шаг 4: Ожидаем результат
        self.calculator_page.wait_for_result("15")

        # Проверяем результат
        actual_result = self.calculator_page.get_result()
        assert actual_result == "15", f"Ожидался результат '15', но получено '{actual_result}'"

def test_calculator_simple():

    driver = webdriver.Chrome()
    try:
        calculator_page = CalculatorPage(driver)

        calculator_page.open()
        calculator_page.set_delay(45)
        calculator_page.click_button("7")
        calculator_page.click_button("+")
        calculator_page.click_button("8")
        calculator_page.click_button("=")
        calculator_page.wait_for_result("15")

        result = calculator_page.get_result()
        assert result == "15", f"Ожидался результат '15', но получено '{result}'"
        print(f"Тест пройден! Результат: {result}")

    finally:
        driver.quit()