from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    """Страница корзины"""

    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_page_load(self):
        """Ждет загрузки страницы корзины"""
        self.wait.until(
            EC.presence_of_element_located(self.CART_ITEM)
        )
        return self

    def click_checkout(self):
        """Нажимает кнопку оформления заказа"""
        checkout_btn = self.wait.until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
        )
        checkout_btn.click()
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)