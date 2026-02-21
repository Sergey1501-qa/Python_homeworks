import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSlowCalculator:

    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 50)  # Немного больше 45 секунд
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")

    def teardown_method(self):
        """Очистка после каждого теста"""
        self.driver.quit()

    def test_calculator_with_45_second_delay(self):
        """Тест калькулятора с задержкой 45 секунд"""

        # 1. Вводим значение 45 в поле задержки
        delay_input = self.driver.find_element(By.CSS_SELECTOR, "#delay")
        delay_input.clear()
        delay_input.send_keys("45")

        # 2. Нажимаем кнопки 7, +, 8, =
        # Находим все кнопки калькулятора
        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".keys span")

        # Создаем словарь для быстрого поиска кнопок по тексту
        button_map = {}
        for button in buttons:
            text = button.text.strip()
            if text:  # только кнопки с текстом
                button_map[text] = button

        # Нажимаем кнопки в нужной последовательности
        button_map["7"].click()
        button_map["+"].click()
        button_map["8"].click()
        button_map["="].click()

        # 3. Ожидаем результат через 45 секунд
        # Локатор для экрана калькулятора
        screen = self.driver.find_element(By.CSS_SELECTOR, ".screen")

        # Ждем, пока на экране не появится "15"
        # Учитываем, что сначала там может быть промежуточный результат
        self.wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".screen"), "15")
        )

        # 4. Проверяем результат
        result = screen.text
        assert result == "15", f"Ожидался результат '15', но получено '{result}'"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])