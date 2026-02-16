from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
class InventoryPage:
    # Локаторы элементов страницы
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_LIST = (By.CLASS_NAME, "inventory_list")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    BURGER_MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    # Локаторы для элементов товара
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ITEM_BUTTON = (By.CSS_SELECTOR, "button.btn_inventory")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def wait_for_page_load(self):
        """Ожидает загрузки страницы с товарами"""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.INVENTORY_CONTAINER)
            )
            print("✅ Страница с товарами загружена")
            return self
        except TimeoutException:
            print("❌ Таймаут при загрузке страницы с товарами")
            # Сохраняем скриншот для отладки
            self.driver.save_screenshot("inventory_page_error.png")
            raise

    def get_all_items(self):
        return self.driver.find_elements(*self.INVENTORY_ITEMS)

    def get_item_by_name(self, item_name):
        try:
            # Пробуем найти по точному тексту
            xpath = f"//div[contains(@class, 'inventory_item_name') and text()='{item_name}']"
            item_name_element = self.driver.find_element(By.XPATH, xpath)

            # Находим родительский контейнер товара
            item_container = item_name_element.find_element(By.XPATH, "./ancestor::div[@class='inventory_item']")
            print(f"✅ Найден товар: {item_name}")
            return item_container
        except NoSuchElementException:
            print(f"❌ Товар '{item_name}' не найден")
            # Выводим все доступные товары для отладки
            self.print_available_items()
            return None

    def print_available_items(self):
        """Выводит список всех доступных товаров на странице"""
        try:
            items = self.get_all_items()
            print("📋 Доступные товары:")
            for i, item in enumerate(items, 1):
                try:
                    name = item.find_element(*self.ITEM_NAME).text
                    price = item.find_element(*self.ITEM_PRICE).text
                    print(f"  {i}. {name} - {price}")
                except:
                    print(f"  {i}. Не удалось получить название товара")
        except Exception as e:
            print(f"❌ Ошибка при получении списка товаров: {e}")

    def add_item_to_cart(self, item_name):
        print(f"🔍 Поиск товара: '{item_name}'")

        # Находим товар по названию
        item_container = self.get_item_by_name(item_name)

        if not item_container:
            raise Exception(f"Товар '{item_name}' не найден на странице")

        # Находим кнопку добавления в корзину
        try:
            # Ищем кнопку по тексту "Add to cart"
            add_button = item_container.find_element(
                By.XPATH, ".//button[contains(text(), 'Add to cart')]"
            )
            button_text = add_button.text
            print(f"🔘 Найдена кнопка: '{button_text}'")

            # Проверяем, что товар еще не в корзине
            if "Remove" in button_text:
                print(f"⚠️ Товар '{item_name}' уже в корзине")
                return self

            # Нажимаем кнопку
            add_button.click()
            print(f"✅ Товар '{item_name}' добавлен в корзину")

        except NoSuchElementException:
            # Пробуем альтернативный способ поиска кнопки
            try:
                add_button = item_container.find_element(By.CSS_SELECTOR, "button.btn_primary")
                add_button.click()
                print(f"✅ Товар '{item_name}' добавлен в корзину (альтернативный локатор)")
            except NoSuchElementException:
                print(f"❌ Не удалось найти кнопку для товара '{item_name}'")
                raise

        return self

    def add_multiple_items(self, item_names):
        print(f"📦 Добавление товаров: {item_names}")
        for item_name in item_names:
            self.add_item_to_cart(item_name)
            # Небольшая пауза между добавлениями для стабильности
            time.sleep(0.5)
        return self

    def get_cart_count(self):
        try:
            # Ждем появления бейджа корзины
            self.wait.until(
                EC.presence_of_element_located(self.CART_BADGE)
            )
            badge = self.driver.find_element(*self.CART_BADGE)
            count = int(badge.text)
            print(f"🛒 В корзине {count} товар(ов)")
            return count
        except (TimeoutException, NoSuchElementException, ValueError):
            print("🛒 Корзина пуста")
            return 0

    def go_to_cart(self):
        """Переходит в корзину"""
        print("🛒 Переход в корзину...")
        cart_link = self.driver.find_element(*self.CART_LINK)
        cart_link.click()
        return self

    def logout(self):
        """Выполняет выход из системы"""
        print("🚪 Выход из системы...")
        burger_menu = self.driver.find_element(*self.BURGER_MENU)
        burger_menu.click()

        self.wait.until(
            EC.element_to_be_clickable(self.LOGOUT_LINK)
        )

        logout_link = self.driver.find_element(*self.LOGOUT_LINK)
        logout_link.click()
        print("✅ Выход выполнен")
        return self