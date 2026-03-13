"""Page Object для страницы авторизации."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure


class LoginPage:
    """Страница авторизации Sauce Demo."""

    # Локаторы
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")

    def __init__(self, driver):
        """
        Инициализация страницы авторизации.

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Открыть страницу авторизации")
    def open(self) -> 'LoginPage':
        """
        Открывает страницу авторизации.

        Returns:
            LoginPage: Текущий объект страницы
        """
        self.driver.get("https://www.saucedemo.com/")
        self.wait.until(EC.presence_of_element_located(self.USERNAME_INPUT))
        return self

    @allure.step("Ввести имя пользователя: {username}")
    def set_username(self, username: str) -> 'LoginPage':
        """
        Вводит имя пользователя.

        Args:
            username: Имя пользователя для ввода

        Returns:
            LoginPage: Текущий объект страницы
        """
        username_field = self.wait.until(
            EC.element_to_be_clickable(self.USERNAME_INPUT)
        )
        username_field.clear()
        username_field.send_keys(username)
        return self

    @allure.step("Ввести пароль")
    def set_password(self, password: str) -> 'LoginPage':
        """
        Вводит пароль.

        Args:
            password: Пароль для ввода

        Returns:
            LoginPage: Текущий объект страницы
        """
        password_field = self.wait.until(
            EC.element_to_be_clickable(self.PASSWORD_INPUT)
        )
        password_field.clear()
        password_field.send_keys(password)
        return self

    @allure.step("Нажать кнопку Login")
    def click_login(self) -> 'LoginPage':
        """
        Нажимает кнопку входа.

        Returns:
            LoginPage: Текущий объект страницы
        """
        login_button = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        login_button.click()
        return self

    @allure.step("Выполнить авторизацию с username: {username}")
    def login(self, username: str, password: str) -> 'LoginPage':
        """
        Выполняет полный процесс авторизации.

        Args:
            username: Имя пользователя
            password: Пароль

        Returns:
            LoginPage: Текущий объект страницы
        """
        self.set_username(username)
        self.set_password(password)
        self.click_login()
        return self

    @allure.step("Проверить успешность авторизации")
    def is_login_successful(self) -> bool:
        """
        Проверяет успешность авторизации.

        Returns:
            bool: True если авторизация успешна, иначе False
        """
        try:
            self.wait.until(EC.presence_of_element_located(self.INVENTORY_LIST))
            return True
        except TimeoutException:
            return False

    @allure.step("Получить текст сообщения об ошибке")
    def get_error_message(self) -> str:
        """
        Получает сообщение об ошибке.

        Returns:
            str: Текст сообщения об ошибке или пустая строка
        """
        try:
            error_element = self.wait.until(
                EC.presence_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text
        except TimeoutException:
            return ""
