from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import re


class CheckoutPage:
    # Локаторы для страницы с информацией о покупателе
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON = (By.ID, "cancel")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    # Локаторы для страницы обзора заказа
    SUMMARY_INFO = (By.CLASS_NAME, "summary_info")
    SUBTOTAL_LABEL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL = (By.CLASS_NAME, "summary_tax_label")
    TOTAL_LABEL = (By.CLASS_NAME, "summary_total_label")
    FINISH_BUTTON = (By.ID, "finish")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    # Локаторы для страницы завершения заказа
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_checkout_info(self):
        """Ожидает загрузки страницы с формой ввода данных"""
        self.wait.until(
            EC.presence_of_element_located(self.FIRST_NAME_INPUT)
        )
        print("✅ Страница оформления заказа загружена")
        return self

    def set_first_name(self, first_name):
        first_name_field = self.driver.find_element(*self.FIRST_NAME_INPUT)
        first_name_field.clear()
        first_name_field.send_keys(first_name)
        return self

    def set_last_name(self, last_name):
        last_name_field = self.driver.find_element(*self.LAST_NAME_INPUT)
        last_name_field.clear()
        last_name_field.send_keys(last_name)
        return self

    def set_postal_code(self, postal_code):
        postal_code_field = self.driver.find_element(*self.POSTAL_CODE_INPUT)
        postal_code_field.clear()
        postal_code_field.send_keys(postal_code)
        return self

    def fill_checkout_info(self, first_name, last_name, postal_code):
        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_postal_code(postal_code)
        print(f"✅ Форма заполнена: {first_name} {last_name}, {postal_code}")
        return self

    def click_continue(self):
        """Нажимает кнопку Continue для перехода к обзору заказа"""
        continue_button = self.driver.find_element(*self.CONTINUE_BUTTON)
        continue_button.click()
        print("✅ Нажата кнопка Continue")
        return self

    def click_cancel(self):
        """Отменяет оформление заказа"""
        cancel_button = self.driver.find_element(*self.CANCEL_BUTTON)
        cancel_button.click()
        print("✅ Оформление отменено")
        return self

    def get_error_message(self):
        try:
            error_element = self.driver.find_element(*self.ERROR_MESSAGE)
            return error_element.text
        except NoSuchElementException:
            return ""

    def wait_for_summary_page(self):
        """Ожидает загрузки страницы с итогами заказа"""
        self.wait.until(
            EC.presence_of_element_located(self.TOTAL_LABEL)
        )
        print("✅ Страница с итогами загружена")
        return self

    def get_item_total(self):
        subtotal_element = self.driver.find_element(*self.SUBTOTAL_LABEL)
        return subtotal_element.text

    def get_tax(self):
        tax_element = self.driver.find_element(*self.TAX_LABEL)
        return tax_element.text

    def get_total(self):
        total_element = self.driver.find_element(*self.TOTAL_LABEL)
        return total_element.text

    def get_total_amount(self):
        total_text = self.get_total()
        print(f"Текст итога: {total_text}")

        # Извлекаем число из текста (формат "Total: $51.79")
        if "$" in total_text:
            amount = total_text.split("$")[1]
            print(f"Извлеченная сумма: {amount}")
            return amount
        else:
            # Если формат другой, ищем число
            numbers = re.findall(r"\d+\.\d+", total_text)
            if numbers:
                return numbers[0]
            else:
                print("❌ Не удалось извлечь сумму из текста")
                return "0.00"

    def click_finish(self):
        """Завершает оформление заказа"""
        finish_button = self.driver.find_element(*self.FINISH_BUTTON)
        finish_button.click()
        print("✅ Заказ оформлен")
        return self

    def wait_for_complete_page(self):
        """Ожидает загрузки страницы завершения заказа"""
        self.wait.until(
            EC.presence_of_element_located(self.COMPLETE_HEADER)
        )
        print("✅ Страница завершения заказа загружена")
        return self

    def get_complete_header(self):
        header = self.driver.find_element(*self.COMPLETE_HEADER)
        return header.text

    def back_home(self):
        """Возвращается на главную страницу"""
        back_button = self.driver.find_element(*self.BACK_HOME_BUTTON)
        back_button.click()
        print("✅ Возврат на главную")
        return self