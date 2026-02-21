"""Page Object для страницы с товарами"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class InventoryPage:
    """Страница с товарами"""

    # Локаторы
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    INVENTORY_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    INVENTORY_ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button.btn_inventory")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_page_load(self):
        """Ждет загрузки страницы"""
        self.wait.until(
            EC.presence_of_element_located(self.INVENTORY_CONTAINER)
        )
        return self

    def get_all_products(self):
        """
        Получает список всех товаров на странице

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

    def add_product_to_cart_by_name(self, product_name):
        """
        Добавляет товар в корзину по названию

        Args:
            product_name: Название товара для добавления

        Returns:
            InventoryPage: Текущий объект страницы
        """
        try:
            # Ждем загрузки всех товаров
            self.wait.until(
                EC.presence_of_all_elements_located(self.INVENTORY_ITEM)
            )

            # Находим все товары
            items = self.driver.find_elements(*self.INVENTORY_ITEM)

            product_found = False
            for item in items:
                try:
                    name_element = item.find_element(*self.INVENTORY_ITEM_NAME)
                    if name_element.text == product_name:
                        # Находим кнопку добавления внутри этого товара
                        add_button = item.find_element(*self.ADD_TO_CART_BUTTON)
                        # Прокручиваем к элементу для надежности
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView(true);", add_button
                        )
                        # Ждем что кнопка кликабельна
                        self.wait.until(EC.element_to_be_clickable(add_button))
                        add_button.click()
                        product_found = True
                        print(f"Товар '{product_name}' добавлен в корзину")
                        break
                except Exception as e:
                    print(f"Ошибка при обработке товара: {e}")
                    continue

            if not product_found:
                raise Exception(f"Товар '{product_name}' не найден на странице")

        except TimeoutException:
            raise Exception("Не удалось загрузить список товаров")

        return self

    def add_product_to_cart_by_index(self, index):
        """
        Добавляет товар в корзину по индексу

        Args:
            index: Индекс товара (начиная с 0)

        Returns:
            InventoryPage: Текущий объект страницы
        """
        items = self.driver.find_elements(*self.INVENTORY_ITEM)
        if index < len(items):
            add_button = items[index].find_element(*self.ADD_TO_CART_BUTTON)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", add_button)
            add_button.click()
        return self

    def get_cart_count(self):
        """Получает количество товаров в корзине"""
        try:
            # Ждем обновления счетчика
            self.wait.until(
                EC.presence_of_element_located(self.SHOPPING_CART_BADGE)
            )
            badge = self.driver.find_element(*self.SHOPPING_CART_BADGE)
            return int(badge.text)
        except TimeoutException:
            return 0
        except Exception:
            return 0

    def go_to_cart(self):
        """Переходит в корзину"""
        cart_link = self.wait.until(
            EC.element_to_be_clickable(self.SHOPPING_CART_LINK)
        )
        cart_link.click()

        # Импортируем здесь чтобы избежать циклических импортов
        from pages.cart_page import CartPage
        return CartPage(self.driver)