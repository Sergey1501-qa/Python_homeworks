from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class CalculatorPage:
    # Локаторы элементов страницы
    DELAY_INPUT = (By.CSS_SELECTOR, "#delay")
    SCREEN = (By.CSS_SELECTOR, ".screen")
    BUTTON_TEMPLATE = (By.XPATH, "//span[text()='{}']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 50)  # Ждем до 50 секунд

    def open(self):
        """Открывает страницу калькулятора"""
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        return self

    def set_delay(self, seconds):
        delay_input = self.driver.find_element(*self.DELAY_INPUT)
        delay_input.clear()
        delay_input.send_keys(str(seconds))
        return self

    def click_button(self, button_text):
        button_locator = (By.XPATH, f"//span[text()='{button_text}']")
        button = self.driver.find_element(*button_locator)
        button.click()
        return self

    def get_result(self):
        screen = self.driver.find_element(*self.SCREEN)
        return screen.text

    def wait_for_result(self, expected_result, timeout=None):
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
        else:
            wait = self.wait

        wait.until(
            EC.text_to_be_present_in_element(self.SCREEN, expected_result)
        )
        return self

    def perform_calculation(self, expression, expected_result):
        for char in expression:
            self.click_button(char)

        # Ожидаем результат
        self.wait_for_result(expected_result)

        # Получаем фактический результат
        actual_result = self.get_result()

        return actual_result == expected_result


# Альтернативная версия с более специализированными методами
class CalculatorPageDetailed:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 50)

    # Локаторы
    DELAY_INPUT = (By.ID, "delay")
    RESULT_SCREEN = (By.CLASS_NAME, "screen")
    BUTTONS_CONTAINER = (By.CLASS_NAME, "keys")

    def open(self):
        """Открывает страницу калькулятора"""
        self.driver.get("https://bonigarcia.dev/selenium-webdriver-java/slow-calculator.html")
        return self

    def set_delay(self, seconds):
        """Устанавливает задержку"""
        delay_field = self.driver.find_element(*self.DELAY_INPUT)
        delay_field.clear()
        delay_field.send_keys(str(seconds))
        return self

    def click_digit(self, digit):
        """Нажимает цифру"""
        self._click_button(str(digit))
        return self

    def click_operator(self, operator):
        """Нажимает оператор (+, -, *, /)"""
        self._click_button(operator)
        return self

    def click_equals(self):
        """Нажимает кнопку равно"""
        self._click_button("=")
        return self

    def _click_button(self, button_text):
        """Внутренний метод для нажатия кнопки"""
        xpath = f"//div[@class='keys']//span[text()='{button_text}']"
        button = self.driver.find_element(By.XPATH, xpath)
        button.click()

    def get_displayed_value(self):
        """Возвращает значение"""
        screen = self.driver.find_element(*self.RESULT_SCREEN)
        return screen.text

    def wait_for_value(self, expected_value, timeout=None):
        """Ожидает появления значения """
        wait_time = timeout or 50
        wait = WebDriverWait(self.driver, wait_time)
        wait.until(
            EC.text_to_be_present_in_element(self.RESULT_SCREEN, expected_value)
        )
        return self