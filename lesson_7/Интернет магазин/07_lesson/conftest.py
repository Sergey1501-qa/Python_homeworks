import pytest
from selenium import webdriver
@pytest.fixture
def firefox_driver():
    """Фикстура для создания Firefox драйвера"""
    driver = webdriver.Firefox()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def login_page(firefox_driver):
    """Фикстура для страницы авторизации"""
    from pages.login_page import LoginPage
    return LoginPage(firefox_driver)


@pytest.fixture
def inventory_page(firefox_driver):
    """Фикстура для страницы инвентаря"""
    from pages.inventory_page import InventoryPage
    return InventoryPage(firefox_driver)


@pytest.fixture
def cart_page(firefox_driver):
    """Фикстура для страницы корзины"""
    from pages.cart_page import CartPage
    return CartPage(firefox_driver)


@pytest.fixture
def checkout_page(firefox_driver):
    """Фикстура для страницы оформления заказа"""
    from pages.checkout_page import CheckoutPage
    return CheckoutPage(firefox_driver)


@pytest.fixture
def all_pages(firefox_driver):
    """Фикстура, возвращающая все страницы"""
    from pages.login_page import LoginPage
    from pages.inventory_page import InventoryPage
    from pages.cart_page import CartPage
    from pages.checkout_page import CheckoutPage

    return {
        'login': LoginPage(firefox_driver),
        'inventory': InventoryPage(firefox_driver),
        'cart': CartPage(firefox_driver),
        'checkout': CheckoutPage(firefox_driver)
    }