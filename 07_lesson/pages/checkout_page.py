"""Page Object для страницы оформления заказа"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    """Страница оформления заказа"""

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
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_checkout_page(self):
        """Ждет загрузки страницы оформления (шаг 1)"""
        self.wait.until(
            EC.presence_of_element_located(self.FIRST_NAME)
        )
        return self

    def fill_customer_info(self, first_name, last_name, postal_code):
        """
        Заполняет информацию о покупателе

        Args:
            first_name: Имя
            last_name: Фамилия
            postal_code: Почтовый индекс
        """
        self.driver.find_element(*self.FIRST_NAME).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE).send_keys(postal_code)
        return self

    def click_continue(self):
        """Нажимает кнопку Continue"""
        continue_btn = self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        )
        continue_btn.click()
        return self

    def wait_for_summary(self):
        """Ждет загрузки страницы с итогами (шаг 2)"""
        self.wait.until(
            EC.presence_of_element_located(self.SUMMARY_INFO)
        )
        return self

    def get_total_amount(self):
        """
        Получает итоговую сумму

        Returns:
            str: Сумма в формате "58.29"
        """
        total_element = self.wait.until(
            EC.presence_of_element_located(self.SUMMARY_TOTAL)
        )
        total_text = total_element.text
        # Извлекаем число из формата "Total: $58.29"
        return total_text.split("$")[1]

    def get_subtotal(self):
        """Получает сумму без налога"""
        subtotal_element = self.driver.find_element(*self.SUMMARY_SUBTOTAL)
        subtotal_text = subtotal_element.text
        return subtotal_text.split("$")[1]

    def click_finish(self):
        """Завершает покупку"""
        finish_btn = self.wait.until(
            EC.element_to_be_clickable(self.FINISH_BUTTON)
        )
        finish_btn.click()
        return self