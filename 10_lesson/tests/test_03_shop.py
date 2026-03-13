"""Тест для интернет-магазина Sauce Demo."""
import allure
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@allure.feature("Интернет-магазин")
@allure.severity(allure.severity_level.CRITICAL)
class TestSauceDemoShop:
    """Тесты для интернет-магазина Saucedemo."""

    def setup_method(self) -> None:
        """Подготовка перед каждым тестом."""
        firefox_options = Options()
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        firefox_options.accept_insecure_certs = True

        self.driver = webdriver.Firefox(options=firefox_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        print("✓ Firefox драйвер запущен")

    def teardown_method(self) -> None:
        """Очистка после каждого теста."""
        if self.driver:
            if hasattr(self, '_outcome') and self._outcome.errors:
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG
                )
            self.driver.quit()
            print("✓ Драйвер закрыт")

    @allure.title("Проверка итоговой суммы покупки")
    @allure.description("Тест проверяет итоговую сумму при покупке трех товаров")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_purchase_total_amount(self) -> None:
        """Тест проверки итоговой суммы покупки."""
        with allure.step("Авторизация"):
            login_page = LoginPage(self.driver)
            login_page.open()
            login_page.login("standard_user", "secret_sauce")
            assert login_page.is_login_successful()
            print("✓ Авторизация успешна")

        with allure.step("Добавление товаров"):
            inventory_page = InventoryPage(self.driver)
            inventory_page.wait_for_page_load()

            products = [
                "Sauce Labs Backpack",
                "Sauce Labs Bolt T-Shirt",
                "Sauce Labs Onesie"
            ]

            for product in products:
                inventory_page.add_product_to_cart_by_name(product)
                print(f"✓ Добавлен товар: {product}")

            cart_count = inventory_page.get_cart_count()
            assert cart_count == 3
            print(f"✓ В корзине {cart_count} товара")

        with allure.step("Оформление заказа"):
            cart_page = inventory_page.go_to_cart()
            cart_page.wait_for_page_load()
            print("✓ Перешли в корзину")

            checkout_page = cart_page.click_checkout()
            checkout_page.wait_for_checkout_page()
            checkout_page.fill_customer_info("Иван", "Петров", "123456")
            checkout_page.click_continue()
            print("✓ Форма заполнена")

            checkout_page.wait_for_summary()
            total = checkout_page.get_total_amount()
            print(f"✓ Итоговая сумма: ${total}")

        with allure.step("Проверка результата"):
            assert total == "58.29"
            print("✓ Тест пройден!")
