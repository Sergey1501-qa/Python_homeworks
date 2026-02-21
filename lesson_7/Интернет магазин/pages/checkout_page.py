from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    """Страница оформления заказа"""

    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    SUMMARY_TOTAL = (By.CLASS_NAME, "summary_total_label")
    SUMMARY_INFO = (By.CLASS_NAME, "summary_info")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_checkout_page(self):
        """Ждет загрузки страницы оформления"""
        self.wait.until(
            EC.presence_of_element_located(self.FIRST_NAME)
        )
        return self

    def fill_customer_info(self, first_name, last_name, postal_code):
        """Заполняет информацию о покупателе"""
        self.driver.find_element(*self.FIRST_NAME).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME).send_keys(last_name)
        self.driver.find_element(*self.POSTAL_CODE).send_keys(postal_code)
        return self

    def click_continue(self):
        """Нажимает кнопку Continue"""
        continue_btn = self.driver.find_element(*self.CONTINUE_BUTTON)
        continue_btn.click()
        return self

    def wait_for_summary(self):
        """Ждет загрузки страницы с итогами"""
        self.wait.until(
            EC.presence_of_element_located(self.SUMMARY_INFO)
        )
        return self

    def get_total_amount(self):
        """Получает итоговую сумму"""
        total_element = self.driver.find_element(*self.SUMMARY_TOTAL)
        total_text = total_element.text
        # Извлекаем число из формата "Total: $58.29"
        return total_text.split("$")[1]