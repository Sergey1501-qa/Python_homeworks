from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class LoginPage:
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        """Открывает страницу авторизации и ждет её загрузки"""
        self.driver.get("https://www.saucedemo.com/")
        # Ждем появления поля для ввода имени
        self.wait.until(
            EC.presence_of_element_located(self.USERNAME_INPUT)
        )
        return self

    def set_username(self, username):
        """Вводит имя пользователя с ожиданием элемента"""
        username_field = self.wait.until(
            EC.element_to_be_clickable(self.USERNAME_INPUT)
        )
        username_field.clear()
        username_field.send_keys(username)
        return self

    def set_password(self, password):
        """Вводит пароль с ожиданием элемента"""
        password_field = self.wait.until(
            EC.element_to_be_clickable(self.PASSWORD_INPUT)
        )
        password_field.clear()
        password_field.send_keys(password)
        return self

    def click_login(self):
        """Нажимает кнопку входа с ожиданием"""
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

        # Проверяем успешность авторизации
        if self.is_login_successful():
            return self
        else:
            error_msg = self.get_error_message()
            raise Exception(f"Ошибка авторизации: {error_msg}")

    def get_error_message(self):
        """Получает текст сообщения об ошибке если оно есть"""
        try:
            error_element = self.wait.until(
                EC.presence_of_element_located(self.ERROR_MESSAGE)
            )
            return error_element.text
        except TimeoutException:
            # Нет сообщения об ошибке
            return ""
        except NoSuchElementException:
            return ""

    def is_login_successful(self):
        """Проверяет, успешно ли выполнена авторизация"""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.INVENTORY_LIST)
            )
            return True
        except TimeoutException:
            return False

    def is_error_displayed(self):
        """Проверяет, отображается ли сообщение об ошибке"""
        try:
            error_element = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_element.is_displayed()
        except NoSuchElementException:
            return False


# Пример использования класса в тесте:
def test_login_success():
    from selenium import webdriver

    driver = webdriver.Chrome()
    try:
        login_page = LoginPage(driver)

        # Открываем страницу и выполняем вход
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        # Проверяем успешность входа
        assert login_page.is_login_successful(), "Вход не выполнен успешно"

    finally:
        driver.quit()


def test_login_failure():
    from selenium import webdriver

    driver = webdriver.Chrome()
    try:
        login_page = LoginPage(driver)

        # Пытаемся войти с неверными данными
        login_page.open()
        login_page.login("invalid_user", "wrong_password")

        # Проверяем появление сообщения об ошибке
        assert login_page.is_error_displayed(), "Сообщение об ошибке не отображается"
        assert login_page.get_error_message() != "", "Текст ошибки пустой"

    finally:
        driver.quit()