import sys
import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Добавляем путь к корневой папке
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Пробуем импортировать страницы
try:
    from pages.login_page import LoginPage
    from pages.inventory_page import InventoryPage
    from pages.cart_page import CartPage
    from pages.checkout_page import CheckoutPage

    print("✅ All pages imported successfully")
except ImportError as e:
    print(f"❌ Import error: {e}")
    # Создаем заглушки для теста
    print("Using fallback classes...")


    class LoginPage:
        def __init__(self, driver):
            self.driver = driver

        def open(self):
            self.driver.get("https://www.saucedemo.com/"); return self

        def login(self, username, password):
            self.driver.find_element(By.ID, "user-name").send_keys(username)
            self.driver.find_element(By.ID, "password").send_keys(password)
            self.driver.find_element(By.ID, "login-button").click()
            return self

        def is_login_successful(self):
            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))
                return True
            except:
                return False


    class InventoryPage:
        def __init__(self, driver):
            self.driver = driver

        def wait_for_page_load(self):
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "inventory_list")))
            return self

        def add_item_to_cart(self, item_name):
            xpath = f"//div[text()='{item_name}']/ancestor::div[@class='inventory_item']//button"
            self.driver.find_element(By.XPATH, xpath).click()
            return self

        def add_multiple_items(self, items):
            for item in items: self.add_item_to_cart(item)
            return self

        def get_cart_count(self):
            try:
                return int(self.driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text)
            except:
                return 0

        def go_to_cart(self):
            self.driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
            return self


    class CartPage:
        def __init__(self, driver): self.driver = driver

        def wait_for_page_load(self):
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "checkout")))
            return self

        def click_checkout(self):
            self.driver.find_element(By.ID, "checkout").click()
            return self


    class CheckoutPage:
        def __init__(self, driver): self.driver = driver

        def wait_for_checkout_info(self):
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "first-name")))
            return self

        def fill_checkout_info(self, first, last, zip):
            self.driver.find_element(By.ID, "first-name").send_keys(first)
            self.driver.find_element(By.ID, "last-name").send_keys(last)
            self.driver.find_element(By.ID, "postal-code").send_keys(zip)
            return self

        def click_continue(self):
            self.driver.find_element(By.ID, "continue").click()
            return self

        def wait_for_summary_page(self):
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label")))
            return self

        def get_total_amount(self):
            total = self.driver.find_element(By.CLASS_NAME, "summary_total_label").text
            return total.split("$")[1]


def test_purchase_simple():
    driver = None
    try:
        print("\n🔵 Запуск Firefox...")
        driver = webdriver.Firefox()
        driver.maximize_window()

        # Создаем страницы
        login_page = LoginPage(driver)
        inventory_page = InventoryPage(driver)
        cart_page = CartPage(driver)
        checkout_page = CheckoutPage(driver)

        # Открываем сайт и авторизуемся
        print("📝 Авторизация...")
        login_page.open()
        login_page.login("standard_user", "secret_sauce")

        # Проверяем успешность входа
        assert login_page.is_login_successful(), "Не удалось авторизоваться"
        print("✅ Авторизация успешна")

        # Добавляем товары
        items_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]

        print("📦 Добавление товаров...")
        inventory_page.wait_for_page_load()
        inventory_page.add_multiple_items(items_to_add)

        # Проверяем корзину
        cart_count = inventory_page.get_cart_count()
        assert cart_count == 3, f"В корзине {cart_count} товаров"
        print(f"✅ В корзине {cart_count} товара")

        # Переходим в корзину
        print("🛒 Переход в корзину...")
        inventory_page.go_to_cart()

        # Оформляем заказ
        print("📝 Оформление заказа...")
        cart_page.wait_for_page_load()
        cart_page.click_checkout()

        # Заполняем форму
        print("📝 Заполнение формы...")
        checkout_page.wait_for_checkout_info()
        checkout_page.fill_checkout_info("Иван", "Петров", "123456")
        checkout_page.click_continue()

        # Проверяем итог
        print("💰 Проверка итоговой суммы...")
        checkout_page.wait_for_summary_page()
        total = checkout_page.get_total_amount()

        print(f"Итоговая сумма: ${total}")
        assert total == "58.29", f"Ожидалось $58.29, получено ${total}"

        print("\n✅✅✅ ТЕСТ ПРОЙДЕН!")

    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        if driver:
            driver.save_screenshot("error.png")
            print("Скриншот сохранен как error.png")
        raise
    finally:
        if driver:
            driver.quit()
            print("🔴 Браузер закрыт")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])