"""Page Object для страницы корзины."""
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class CartPage:
    """Страница корзины."""

    # Локаторы
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button.cart_button")

    def __init__(self, driver):
        """
        Инициализация страницы корзины.

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Ожидать загрузки страницы корзины")
    def wait_for_page_load(self) -> 'CartPage':
        """
        Ждет загрузки страницы корзины.

        Returns:
            CartPage: Текущий объект страницы
        """
        self.wait.until(
            EC.presence_of_element_located(self.CART_ITEM)
        )
        return self

    @allure.step("Получить список названий товаров в корзине")
    def get_cart_items(self) -> List[str]:
        """
        Получает список названий товаров в корзине.

        Returns:
            list: Список названий товаров
        """
        items = self.driver.find_elements(*self.CART_ITEM_NAME)
        return [item.text for item in items]

    @allure.step("Нажать кнопку Checkout")
    def click_checkout(self):
        """
        Нажимает кнопку оформления заказа.

        Returns:
            CheckoutPage: Объект страницы оформления заказа
        """
        checkout_btn = self.wait.until(
            EC.element_to_be_clickable(self.CHECKOUT_BUTTON)
        )
        checkout_btn.click()

        # Импортируем здесь чтобы избежать циклических импортов
        from pages.checkout_page import CheckoutPage
        return CheckoutPage(self.driver)

    @allure.step("Удалить товар '{product_name}' из корзины")
    def remove_item(self, product_name: str) -> 'CartPage':
        """
        Удаляет товар из корзины по названию.

        Args:
            product_name: Название товара для удаления

        Returns:
            CartPage: Текущий объект страницы
        """
        xpath = (
            f"//div[@class='inventory_item_name' and text()='{product_name}']"
            f"/ancestor::div[@class='cart_item']"
            f"//button[contains(text(), 'Remove')]"
        )
        remove_btn = self.driver.find_element(By.XPATH, xpath)
        remove_btn.click()
        return self
