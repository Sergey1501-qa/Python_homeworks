"""Тест для медленного калькулятора"""
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSlowCalculator:
    """Тесты для медленного калькулятора"""

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 50)
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

    def teardown_method(self):
        """Очистка после каждого теста"""
        self.driver.quit()

    def test_calculator_with_45_second_delay(self):
        """
        Тест калькулятора с задержкой 45 секунд

        Шаги:
        1. Установить задержку 45 секунд
        2. Нажать кнопки 7 + 8 =
        3. Подождать результат
        4. Проверить что результат равен 15
        """
        # 1. Вводим значение 45 в поле задержки
        delay_input = self.driver.find_element(By.CSS_SELECTOR, "#delay")
        delay_input.clear()
        delay_input.send_keys("45")

        # 2. Нажимаем кнопки 7 + 8 =
        # Создаем словарь для быстрого доступа к кнопкам
        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".keys span")
        button_map = {}
        for button in buttons:
            text = button.text.strip()
            if text:
                button_map[text] = button

        # Нажимаем кнопки в нужной последовательности
        button_map["7"].click()
        button_map["+"].click()
        button_map["8"].click()
        button_map["="].click()

        # 3. Ожидаем результат через 45 секунд
        screen = self.driver.find_element(By.CSS_SELECTOR, ".screen")

        # Ждем появления результата
        self.wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".screen"), "15")
        )

        # 4. Проверяем результат
        result = screen.text
        assert result == "15", f"Ожидался результат '15', но получено '{result}'"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])