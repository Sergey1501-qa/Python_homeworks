from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:
    """Страница с товарами"""

    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button.btn_inventory")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_page_load(self):
        """Ждет загрузки страницы"""
        self.wait.until(
            EC.presence_of_element_located(self.INVENTORY_ITEM)
        )
        return self

    def add_product_to_cart(self, product_name):
        """Добавляет товар в корзину по названию"""
        xpath = (
            f"//div[@class='inventory_item_name' and text()='{product_name}']"
            f"/ancestor::div[@class='inventory_item']"
        )
        product_item = self.driver.find_element(By.XPATH, xpath)
        add_button = product_item.find_element(*self.ADD_TO_CART_BUTTON)
        add_button.click()
        return self

    def go_to_cart(self):
        """Переходит в корзину"""
        cart_link = self.driver.find_element(*self.SHOPPING_CART_LINK)
        cart_link.click()
        from pages.cart_page import CartPage
        return CartPage(self.driver)