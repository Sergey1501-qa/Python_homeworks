from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:
    """Страница авторизации"""

    # Локаторы
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        """Открывает страницу авторизации"""
        self.driver.get("https://www.saucedemo.com/")
        self.wait.until(
            EC.presence_of_element_located(self.USERNAME_INPUT)
        )
        return self

    def set_username(self, username):
        """Вводит имя пользователя"""
        username_field = self.wait.until(
            EC.element_to_be_clickable(self.USERNAME_INPUT)
        )
        username_field.clear()
        username_field.send_keys(username)
        return self

    def set_password(self, password):
        """Вводит пароль"""
        password_field = self.wait.until(
            EC.element_to_be_clickable(self.PASSWORD_INPUT)
        )
        password_field.clear()
        password_field.send_keys(password)
        return self

    def click_login(self):
        """Нажимает кнопку входа"""
        login_button = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        login_button.click()
        return self

    def login(self, username, password):
        """Выполняет полный процесс авторизации"""
        self.set_username(username)
        self.set_password(password)
        self.click_login()
        return self

    def is_login_successful(self):
        """Проверяет успешность авторизации"""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.INVENTORY_LIST)
            )
            return True
        except TimeoutException:
            return False

    def get_error_message(self):
        """Получает сообщение об ошибке"""
        try:
            error_element = self.wait.until(
                EC.presence_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text
        except TimeoutException:
            return ""