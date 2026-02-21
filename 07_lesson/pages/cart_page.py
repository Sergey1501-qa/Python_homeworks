"""Page Object для страницы корзины"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    """Страница корзины"""

    # Локаторы
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button.cart_button")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_page_load(self):
        """Ждет загрузки страницы корзины"""
        self.wait.until(
            EC.presence_of_element_located(self.CART_ITEM)
        )
        return self

    def get_cart_items(self):
        """Получает список названий товаров в корзине"""
        items = self.driver.find_elements(*self.CART_ITEM_NAME)
        return [item.text for item in items]

    def click_checkout(self):
        """Нажимает кнопку оформления заказа"""
        checkout_btn = self.wait.until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
        )
        checkout_btn.click()

        # Импортируем здесь чтобы избежать циклических импортов
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)

    def remove_item(self, product_name):
        """Удаляет товар из корзины по названию"""
        xpath = (
            f"//div[@class='inventory_item_name' and text()='{product_name}']"
            f"/ancestor::div[@class='cart_item']"
            f"//button[contains(text(), 'Remove')]"
        )
        remove_btn = self.driver.find_element(By.XPATH, xpath)
        remove_btn.click()
        return self