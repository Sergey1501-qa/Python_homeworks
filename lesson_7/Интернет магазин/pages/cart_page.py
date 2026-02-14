from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class CartPage:
    # Локаторы элементов страницы
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button.cart_button")
    CART_ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_page_load(self):
        """Ожидает загрузки страницы корзины"""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.CART_ITEMS)
            )
            print("✅ Страница корзины загружена")
        except TimeoutException:
            print("⚠️ В корзине нет товаров или страница не загрузилась")
        return self

    def get_cart_items(self):
        return self.driver.find_elements(*self.CART_ITEMS)

    def get_cart_item_names(self):
        name_elements = self.driver.find_elements(*self.CART_ITEM_NAMES)
        return [element.text for element in name_elements]

    def remove_item(self, item_name):
        try:
            xpath = f"//div[@class='inventory_item_name' and text()='{item_name}']/ancestor::div[@class='cart_item']//button"
            remove_button = self.driver.find_element(By.XPATH, xpath)
            remove_button.click()
            print(f"✅ Товар '{item_name}' удален из корзины")
        except NoSuchElementException:
            print(f"❌ Товар '{item_name}' не найден в корзине")
            raise
        return self

    def click_checkout(self):
        checkout_button = self.driver.find_element(*self.CHECKOUT_BUTTON)
        checkout_button.click()
        print("✅ Нажата кнопка Checkout")
        return self

    def continue_shopping(self):
        continue_button = self.driver.find_element(*self.CONTINUE_SHOPPING_BUTTON)
        continue_button.click()
        print("✅ Возврат к покупкам")
        return self

    def get_cart_count(self):
        return len(self.get_cart_items())