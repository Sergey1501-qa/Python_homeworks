import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_purchase_with_fixtures(all_pages):
    # Получаем страницы
    login_page = all_pages['login']
    inventory_page = all_pages['inventory']
    cart_page = all_pages['cart']
    checkout_page = all_pages['checkout']

    # Открываем сайт и авторизуемся
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    # Добавляем товары
    inventory_page.wait_for_page_load()
    inventory_page.add_multiple_items([
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt",
        "Sauce Labs Onesie"
    ])

    # Переходим в корзину и оформляем заказ
    inventory_page.go_to_cart()
    cart_page.wait_for_page_load()
    cart_page.click_checkout()

    # Заполняем форму
    checkout_page.wait_for_checkout_info()
    checkout_page.fill_checkout_info("Иван", "Петров", "123456")
    checkout_page.click_continue()

    # Проверяем итог
    checkout_page.wait_for_summary_page()
    total_amount = checkout_page.get_total_amount()

    assert total_amount == "58.29", f"Ожидалась сумма $58.29, получено ${total_amount}"
    print(f"Тест пройден! Итоговая сумма: ${total_amount}")