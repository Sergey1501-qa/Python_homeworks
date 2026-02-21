import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestSauceDemoShop:
    """Тесты для сайта магазина Sauce Demo"""

    def setup_method(self):
        # Используем Firefox как указано в задании
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.get("https://www.saucedemo.com/")

    def teardown_method(self):
        """Очистка после каждого теста"""
        self.driver.quit()

    def test_purchase_total_amount(self):
        """Тест проверки итоговой суммы покупки"""

        # 1. Авторизация как пользователь standard_user
        username_input = self.driver.find_element(By.ID, "user-name")
        password_input = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.ID, "login-button")

        username_input.send_keys("standard_user")
        password_input.send_keys("secret_sauce")
        login_button.click()

        # Ждем загрузки страницы с товарами
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_item"))
        )

        # 2. Добавляем товары в корзину
        # Находим все товары на странице
        items = self.driver.find_elements(By.CLASS_NAME, "inventory_item")

        # Словарь для хранения кнопок добавления в корзину
        add_to_cart_buttons = {}

        # Собираем информацию о товарах и их кнопках
        for item in items:
            item_name = item.find_element(By.CLASS_NAME, "inventory_item_name").text
            button = item.find_element(By.CSS_SELECTOR, "button.btn_inventory")
            add_to_cart_buttons[item_name] = button

        # Добавляем нужные товары в корзину
        required_items = [
            "Sauce Labs Backpack",
            "Sauce Labs Bolt T-Shirt",
            "Sauce Labs Onesie"
        ]

        for item_name in required_items:
            if item_name in add_to_cart_buttons:
                add_to_cart_buttons[item_name].click()
                print(f"Добавлен товар: {item_name}")

        # 3. Переходим в корзину
        cart_icon = self.driver.find_element(By.CLASS_NAME, "shopping_cart_link")
        cart_icon.click()

        # Ждем загрузки страницы корзины
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "cart_item"))
        )

        # 4. Нажимаем Checkout
        checkout_button = self.driver.find_element(By.ID, "checkout")
        checkout_button.click()

        # 5. Заполняем форму данными
        # Ждем загрузки формы
        self.wait.until(
            EC.presence_of_element_located((By.ID, "first-name"))
        )

        # Заполняем поля формы
        first_name_field = self.driver.find_element(By.ID, "first-name")
        last_name_field = self.driver.find_element(By.ID, "last-name")
        postal_code_field = self.driver.find_element(By.ID, "postal-code")

        # Используем тестовые данные
        first_name_field.send_keys("Иван")
        last_name_field.send_keys("Петров")
        postal_code_field.send_keys("123456")

        # 6. Нажимаем Continue
        continue_button = self.driver.find_element(By.ID, "continue")
        continue_button.click()

        # 7. Читаем итоговую стоимость
        # Ждем загрузки страницы с итогами
        self.wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
        )

        # Находим элемент с итоговой стоимостью
        total_element = self.driver.find_element(By.CLASS_NAME, "summary_total_label")
        total_text = total_element.text

        # Извлекаем числовое значение из текста
        # Формат текста: "Total: $58.29"
        total_amount = total_text.split("$")[1]

        # 8. Проверяем, что итоговая сумма равна $58.29
        assert total_amount == "58.29", f"Ожидалась сумма $58.29, но получено ${total_amount}"
        print(f"Тест пройден! Итоговая сумма: ${total_amount}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])