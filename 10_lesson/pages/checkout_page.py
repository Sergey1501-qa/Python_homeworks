"""Page Object для страницы оформления заказа."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class CheckoutPage:
    """Страница оформления заказа."""

    # Локаторы для шага 1 (информация о покупателе)
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")

    # Локаторы для шага 2 (обзор заказа)
    FINISH_BUTTON = (By.ID, "finish")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")
    SUMMARY_INFO = (By.CLASS_NAME, "summary_info")
    SUMMARY_SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    SUMMARY_TAX = (By.CLASS_NAME, "summary_tax_label")

    def __init__(self, driver):
        """
        Инициализация страницы оформления заказа.

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Ожидать загрузки страницы оформления")
    def wait_for_checkout_page(self) -> 'CheckoutPage':
        """
        Ждет загрузки страницы оформления (шаг 1).

        Returns:
            CheckoutPage: Текущий объект страницы
        """
        self.wait.until(
            EC.presence_of_element_located(self.FIRST_NAME)
        )
        return self

    @allure.step("Заполнить информацию о покупателе")
    def fill_customer_info(
        self, first_name: str, last_name: str, postal_code: str
    ) -> 'CheckoutPage':
        """
        Заполняет информацию о покупателе.

        Args:
            first_name: Имя
            last_name: Фамилия
            postal_code: Почтовый индекс

        Returns:
            CheckoutPage: Текущий объект страницы
        """
        with allure.step(f"Ввести имя: {first_name}"):
            self.driver.find_element(*self.FIRST_NAME).send_keys(first_name)

        with allure.step(f"Ввести фамилию: {last_name}"):
            self.driver.find_element(*self.LAST_NAME).send_keys(last_name)

        with allure.step(f"Ввести почтовый индекс: {postal_code}"):
            self.driver.find_element(*self.POSTAL_CODE).send_keys(postal_code)

        return self

    @allure.step("Нажать кнопку Continue")
    def click_continue(self) -> 'CheckoutPage':
        """
        Нажимает кнопку Continue.

        Returns:
            CheckoutPage: Текущий объект страницы
        """
        continue_btn = self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        )
        continue_btn.click()
        return self

    @allure.step("Ожидать загрузки страницы с итогами")
    def wait_for_summary(self) -> 'CheckoutPage':
        """
        Ждет загрузки страницы с итогами (шаг 2).

        Returns:
            CheckoutPage: Текущий объект страницы
        """
        self.wait.until(
            EC.presence_of_element_located(self.SUMMARY_INFO)
        )
        return self

    @allure.step("Получить итоговую сумму")
    def get_total_amount(self) -> str:
        """
        Получает итоговую сумму.

        Returns:
            str: Сумма в формате "58.29"
        """
        total_element = self.wait.until(
            EC.presence_of_element_located(self.SUMMARY_TOTAL)
        )
        total_text = total_element.text
        return total_text.split("$")[1]

    @allure.step("Получить сумму без налога")
    def get_subtotal(self) -> str:
        """
        Получает сумму без налога.

        Returns:
            str: Сумма без налога в формате "58.29"
        """
        subtotal_element = self.driver.find_element(*self.SUMMARY_SUBTOTAL)
        subtotal_text = subtotal_element.text
        return subtotal_text.split("$")[1]

    @allure.step("Завершить покупку")
    def click_finish(self) -> 'CheckoutPage':
        """
        Завершает покупку.

        Returns:
            CheckoutPage: Текущий объект страницы
        """
        finish_btn = self.wait.until(
            EC.element_to_be_clickable(self.FINISH_BUTTON)
        )
        finish_btn.click()
        return self
