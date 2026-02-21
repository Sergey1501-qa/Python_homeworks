import sys
import os
import pytest
from selenium import webdriver

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

print(f"PROJECT_ROOT: {PROJECT_ROOT}")
print(f"Python path: {sys.path}")

# Импортируем страницы
try:
    from pages.login_page import LoginPage
    from pages.inventory_page import InventoryPage
    from pages.cart_page import CartPage
    from pages.checkout_page import CheckoutPage

    print("✅ Все страницы импортированы успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    raise


class TestSauceDemoShop:
    """Тесты для интернет-магазина Sauce Demo."""

    def setup_method(self):
        """Настройка перед каждым тестом."""
        print("\n🔵 Запуск Firefox...")
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

        # Создаем объекты страниц
        self.login_page = LoginPage(self.driver)
        self.inventory_page = InventoryPage(self.driver)
        self.cart_page = CartPage(self.driver)
        self.checkout_page = CheckoutPage(self.driver)
        print("✅ Страницы инициализированы")

    def teardown_method(self):
        """Очистка после каждого теста."""
        if hasattr(self, 'driver'):
            print("🔴 Закрытие браузера...")
            self.driver.quit()

    def test_purchase_total_amount(self):
        """
        Тест проверки итоговой суммы покупки.
        Ожидаемая сумма: $58.29
        """
        # Шаг 1-2: Открыть сайт и авторизоваться
        print("\n📝 Шаг 1-2: Авторизация")
        self.login_page.open()
        self.login_page.login("standard_user", "secret_sauce")

        # Проверяем успешность входа
        assert self.login_page.is_login_successful(), "❌ Не удалось авторизоваться"
        print("✅ Авторизация успешна")

        # Шаг 3: Добавить товары в корзину
        print("\n📝 Шаг 3: Добавление товаров в корзину")
        items_to_add = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]

        print("⏳ Ожидание загрузки страницы с товарами...")
        self.inventory_page.wait_for_page_load()

        # Для отладки выведем все доступные товары
        self.inventory_page.print_available_items()

        print(f"📦 Добавление товаров: {items_to_add}")
        self.inventory_page.add_multiple_items(items_to_add)

        # Проверяем, что в корзине 3 товара
        cart_count = self.inventory_page.get_cart_count()
        assert cart_count == 3, f"❌ В корзине должно быть 3 товара, а сейчас {cart_count}"
        print(f"✅ В корзине {cart_count} товара")

        # Шаг 4: Перейти в корзину
        print("\n📝 Шаг 4: Переход в корзину")
        self.inventory_page.go_to_cart()

        # Шаг 5: Нажать Checkout
        print("\n📝 Шаг 5: Оформление заказа")
        self.cart_page.wait_for_page_load()
        self.cart_page.click_checkout()

        # Шаг 6: Заполнить форму данными
        print("\n📝 Шаг 6: Заполнение формы")
        self.checkout_page.wait_for_checkout_info()
        self.checkout_page.fill_checkout_info(
            first_name="Иван",
            last_name="Петров",
            postal_code="123456"
        )
        self.checkout_page.click_continue()

        # Шаг 7-8: Прочитать итоговую стоимость и проверить
        print("\n📝 Шаг 7-8: Проверка итоговой суммы")
        self.checkout_page.wait_for_summary_page()

        total_amount = self.checkout_page.get_total_amount()
        total_text = self.checkout_page.get_total()

        print(f"\n💰 Итоговая стоимость: {total_text}")
        print(f"💰 Числовое значение: {total_amount}")

        # Проверяем, что итоговая сумма равна $58.29
        expected_total = "58.29"
        assert total_amount == expected_total, \
            f"❌ Ожидалась сумма ${expected_total}, но получено ${total_amount}"

        print(f"\n✅✅✅ ТЕСТ ПРОЙДЕН! Итоговая сумма: ${total_amount}")


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


# Для запуска через python напрямую
if __name__ == "__main__":
    # Запускаем простой тест
    test_purchase_simple()
