"""Тест для медленного калькулятора"""
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@allure.feature("Калькулятор")
@allure.severity(allure.severity_level.NORMAL)
@allure.story("Медленный калькулятор")
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
        if self.driver:
            if hasattr(self, '_outcome') and self._outcome.errors:
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG
                )
            self.driver.quit()

    @allure.title("Тест калькулятора с задержкой 45 секунд")
    @allure.description("""
        Тест проверяет работу калькулятора с установленной задержкой 45 секунд.

        Шаги:
        1. Установить значение задержки 45 секунд
        2. Нажать кнопки 7, +, 8, =
        3. Дождаться появления результата
        4. Проверить что результат равен 15
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.tag("smoke", "calculator")
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
        with allure.step("Шаг 1: Установка задержки 45 секунд"):
            delay_input = self.driver.find_element(By.CSS_SELECTOR, "#delay")
            delay_input.clear()
            delay_input.send_keys("45")
            allure.attach(
                "Установлена задержка 45 секунд",
                name="delay_value",
                attachment_type=allure.attachment_type.TEXT
            )

        # 2. Нажимаем кнопки 7 + 8 =
        with allure.step("Шаг 2: Нажатие кнопок 7 + 8 ="):
            # Создаем словарь для быстрого доступа к кнопкам
            buttons = self.driver.find_elements(By.CSS_SELECTOR, ".keys span")
            button_map = {}
            for button in buttons:
                text = button.text.strip()
                if text:
                    button_map[text] = button

            # Нажимаем кнопки в нужной последовательности
            button_map["7"].click()
            allure.attach("Нажата кнопка 7", name="button_press", attachment_type=allure.attachment_type.TEXT)

            button_map["+"].click()
            allure.attach("Нажата кнопка +", name="button_press", attachment_type=allure.attachment_type.TEXT)

            button_map["8"].click()
            allure.attach("Нажата кнопка 8", name="button_press", attachment_type=allure.attachment_type.TEXT)

            button_map["="].click()
            allure.attach("Нажата кнопка =", name="button_press", attachment_type=allure.attachment_type.TEXT)

        # 3. Ожидаем результат через 45 секунд
        with allure.step("Шаг 3: Ожидание результата"):
            screen = self.driver.find_element(By.CSS_SELECTOR, ".screen")

            # Ждем появления результата
            self.wait.until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".screen"), "15")
            )

            # Получаем результат
            result = screen.text
            allure.attach(
                f"Получен результат: {result}",
                name="calculation_result",
                attachment_type=allure.attachment_type.TEXT
            )

        # 4. Проверяем результат
        with allure.step("Шаг 4: Проверка результата"):
            assert result == "15", f"Ожидался результат '15', но получено '{result}'"
            allure.attach(
                "Результат соответствует ожидаемому значению 15",
                name="verification_result",
                attachment_type=allure.attachment_type.TEXT
            )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--alluredir=allure-results"])
