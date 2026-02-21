import pytest
from selenium import webdriver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage


class TestSauceDemoShop:
    """Тесты для интернет-магазина Saucedemo"""

    def setup_method(self):
        """Подготовка перед каждым тестом"""
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def teardown_method(self):
        """Очистка после каждого теста"""
        self.driver.quit()

    def test_purchase_total_amount(self):
        """
        Тест проверки итоговой суммы покупки
        Шаги:
        1. Авторизация
        2. Добавление товаров в корзину
        3. Переход в корзину
        4. Заполнение формы
        5. Проверка итоговой суммы
        """
        # 1. Авторизация
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.login("standard_user", "secret_sauce")
        assert login_page.is_login_successful(), "Не удалось авторизоваться"

        # 2. Добавление товаров в корзину
        inventory_page = InventoryPage(self.driver)
        inventory_page.wait_for_page_load()

        products_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]

        for product in products_to_add:
            inventory_page.add_product_to_cart(product)

        # 3. Переход в корзину и оформление заказа
        cart_page = inventory_page.go_to_cart()
        cart_page.wait_for_page_load()
        checkout_page = cart_page.click_checkout()

        # 4. Заполнение формы
        checkout_page.wait_for_checkout_page()
        checkout_page.fill_customer_info("Иван", "Петров", "123456")
        checkout_page.click_continue()

        # 5. Проверка итоговой суммы
        checkout_page.wait_for_summary()
        total_amount = checkout_page.get_total_amount()

        expected_total = "58.29"
        assert total_amount == expected_total, (
            f"Ожидалась сумма ${expected_total}, "
            f"получено ${total_amount}"
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v"])