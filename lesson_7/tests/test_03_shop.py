"""Тест для интернет-магазина Sauce Demo"""
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage


class TestSauceDemoShop:
    """Тесты для интернет-магазина Saucedemo"""

    def setup_method(self):
        """Подготовка перед каждым тестом"""
        # Настройки для Firefox
        firefox_options = Options()
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")

        # Запуск Firefox
        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(5)  # Неявное ожидание для надежности

    def teardown_method(self):
        """Очистка после каждого теста"""
        if self.driver:
            self.driver.quit()

    def test_purchase_total_amount(self):
        """
        Тест проверки итоговой суммы покупки

        Шаги:
        1. Открыть страницу авторизации
        2. Авторизоваться как standard_user
        3. Добавить в корзину 3 товара
        4. Перейти в корзину
        5. Нажать Checkout
        6. Заполнить форму данными
        7. Нажать Continue
        8. Прочитать итоговую стоимость
        9. Проверить что сумма равна $58.29
        """
        try:
            # 1-2. Открытие страницы и авторизация
            print("\n=== Шаг 1-2: Авторизация ===")
            login_page = LoginPage(self.driver)
            login_page.open()
            login_page.login("standard_user", "secret_sauce")

            # Проверяем успешность авторизации
            assert login_page.is_login_successful(), "Не удалось авторизоваться"
            print("✓ Авторизация успешна")

            # 3. Добавление товаров в корзину
            print("\n=== Шаг 3: Добавление товаров в корзину ===")
            inventory_page = InventoryPage(self.driver)
            inventory_page.wait_for_page_load()

            # Показываем все доступные товары
            all_products = inventory_page.get_all_products()
            print("Доступные товары:")
            for i, product in enumerate(all_products):
                print(f"  {i+1}. {product['name']} - {product['price']}")

            # Список товаров для добавления
            products_to_add = [
                "Sauce Labs Backpack",
                "Sauce Labs Bolt T-Shirt",
                "Sauce Labs Onesie"
            ]

            # Добавляем каждый товар
            for product in products_to_add:
                inventory_page.add_product_to_cart_by_name(product)
                print(f"✓ Добавлен товар: {product}")

            # Проверяем что добавили 3 товара
            cart_count = inventory_page.get_cart_count()
            assert cart_count == 3, f"Ожидалось 3 товара, получено {cart_count}"
            print(f"✓ В корзине {cart_count} товара")

            # 4. Переход в корзину
            print("\n=== Шаг 4: Переход в корзину ===")
            cart_page = inventory_page.go_to_cart()
            cart_page.wait_for_page_load()
            print("✓ Перешли в корзину")

            # 5. Нажатие Checkout
            print("\n=== Шаг 5: Оформление заказа ===")
            checkout_page = cart_page.click_checkout()
            print("✓ Нажали Checkout")

            # 6-7. Заполнение формы и Continue
            print("\n=== Шаг 6-7: Заполнение формы ===")
            checkout_page.wait_for_checkout_page()
            checkout_page.fill_customer_info("Иван", "Петров", "123456")
            checkout_page.click_continue()
            print("✓ Форма заполнена")

            # 8. Чтение итоговой стоимости
            print("\n=== Шаг 8: Получение итоговой суммы ===")
            checkout_page.wait_for_summary()
            total_amount = checkout_page.get_total_amount()
            print(f"✓ Итоговая сумма: ${total_amount}")

            # 9. Проверка итоговой суммы
            print("\n=== Шаг 9: Проверка результата ===")
            expected_total = "58.29"
            assert total_amount == expected_total, (
                f"Ожидалась сумма ${expected_total}, "
                f"получено ${total_amount}"
            )
            print(f"✓ Тест пройден! Сумма ${total_amount} соответствует ожидаемой")

        except Exception as e:
            # Делаем скриншот при ошибке
            self.driver.save_screenshot("error_screenshot.png")
            print(f"\n❌ Ошибка: {e}")
            raise


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])