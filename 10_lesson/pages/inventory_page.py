"""Page Object для страницы с товарами."""
from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure


class InventoryPage:
    """Страница с товарами."""

    # Локаторы
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    INVENTORY_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    INVENTORY_ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button.btn_inventory")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver):
        """
        Инициализация страницы с товарами.

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step("Ожидать загрузки страницы с товарами")
    def wait_for_page_load(self) -> 'InventoryPage':
        """
        Ждет загрузки страницы.

        Returns:
            InventoryPage: Текущий объект страницы
        """
        self.wait.until(
            EC.presence_of_element_located(self.INVENTORY_CONTAINER)
        )
        return self

    @allure.step("Получить список всех товаров")
    def get_all_products(self) -> List[Dict[str, str]]:
        """
        Получает список всех товаров на странице.

        Returns:
            list: Список словарей с информацией о товарах
        """
        products = []
        items = self.driver.find_elements(*self.INVENTORY_ITEM)

        for item in items:
            name = item.find_element(*self.INVENTORY_ITEM_NAME).text
            price = item.find_element(*self.INVENTORY_ITEM_PRICE).text
            products.append({"name": name, "price": price})

        return products

    @allure.step("Добавить товар '{product_name}' в корзину")
    def add_product_to_cart_by_name(self, product_name: str) -> 'InventoryPage':
        """
        Добавляет товар в корзину по названию.

        Args:
            product_name: Название товара для добавления

        Returns:
            InventoryPage: Текущий объект страницы

        Raises:
            Exception: Если товар не найден
        """
        try:
            self.wait.until(
                EC.presence_of_all_elements_located(self.INVENTORY_ITEM)
            )
            items = self.driver.find_elements(*self.INVENTORY_ITEM)
            product_found = False

            for item in items:
                name_element = item.find_element(*self.INVENTORY_ITEM_NAME)
                if name_element.text == product_name:
                    add_button = item.find_element(*self.ADD_TO_CART_BUTTON)
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView(true);", add_button
                    )
                    self.wait.until(EC.element_to_be_clickable(add_button))
                    add_button.click()
                    product_found = True
                    break

            if not product_found:
                raise Exception(f"Товар '{product_name}' не найден")

        except TimeoutException as exc:
            raise Exception("Не удалось загрузить список товаров") from exc

        return self

    @allure.step("Добавить товар по индексу {index}")
    def add_product_to_cart_by_index(self, index: int) -> 'InventoryPage':
        """
        Добавляет товар в корзину по индексу.

        Args:
            index: Индекс товара (начиная с 0)

        Returns:
            InventoryPage: Текущий объект страницы
        """
        items = self.driver.find_elements(*self.INVENTORY_ITEM)
        if index < len(items):
            add_button = items[index].find_element(*self.ADD_TO_CART_BUTTON)
            self.driver.execute_script(
                "arguments[0].scrollIntoView(true);", add_button
            )
            add_button.click()
        return self

    @allure.step("Получить количество товаров в корзине")
    def get_cart_count(self) -> int:
        """
        Получает количество товаров в корзине.

        Returns:
            int: Количество товаров в корзине
        """
        try:
            self.wait.until(
                EC.presence_of_element_located(self.SHOPPING_CART_BADGE)
            )
            badge = self.driver.find_element(*self.SHOPPING_CART_BADGE)
            return int(badge.text)
        except (TimeoutException, ValueError):
            return 0

    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        """
        Переходит в корзину.

        Returns:
            CartPage: Объект страницы корзины
        """
        cart_link = self.wait.until(
            EC.element_to_be_clickable(self.SHOPPING_CART_LINK)
        )
        cart_link.click()

        from pages.cart_page import CartPage
        return CartPage(self.driver)
