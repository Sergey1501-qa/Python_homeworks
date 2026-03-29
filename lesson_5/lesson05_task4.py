from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def login_form_firefox():

    print("=" * 70)
    print("УПРАЖНЕНИЕ 4: Форма авторизации (FireFox)")
    print("=" * 70)

    driver = None
    try:
        # === ШАГ 1: ОТКРЫТЬ MOZILLA FIREFOX ===
        print("\n1. Открытие браузера Mozilla Firefox...")

        firefox_options = Options()
        firefox_options.add_argument('--start-maximized')

        try:
            driver = webdriver.Firefox(options=firefox_options)
            print("   ✓ Firefox успешно открыт")
        except Exception as e:
            print(f"   ✗ Ошибка: {e}")
            print("   Пробую ручную настройку...")

            firefox_driver_path = r"C:\WebDriver\geckodriver.exe"
            service = Service(firefox_driver_path)
            driver = webdriver.Firefox(service=service, options=firefox_options)
            print(f"   ✓ Firefox открыт с драйвером")

        # === ШАГ 2: ПЕРЕЙТИ НА СТРАНИЦУ ===
        print("\n2. Переход на http://the-internet.herokuapp.com/login...")
        driver.get("http://the-internet.herokuapp.com/login")
        print("   ✓ Страница загружена")

        wait = WebDriverWait(driver, 10)

        # === ШАГ 3: ЗАПОЛНИТЬ USERNAME ===
        print("\n3. Заполнение username...")
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.send_keys("tomsmith")
        print(f"   ✓ Введен username: tomsmith")

        # === ШАГ 4: ЗАПОЛНИТЬ PASSWORD ===
        print("\n4. Заполнение password...")
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("SuperSecretPassword!")
        print(f"   ✓ Введен password")

        # Скриншот формы
        driver.save_screenshot("task4_firefox_form.png")
        print("   ✓ Скриншот формы: task4_firefox_form.png")

        # === ШАГ 5: НАЖАТЬ LOGIN ===
        print("\n5. Нажатие кнопки Login...")
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        print("   ✓ Кнопка нажата")

        time.sleep(2)

        # === ШАГ 6: ПОЛУЧИТЬ ТЕКСТ ЗЕЛЕНОЙ ПЛАШКИ ===
        print("\n6. Получение текста зеленой плашки...")

        success_message = wait.until(
            EC.presence_of_element_located((By.ID, "flash"))
        )

        message_text = success_message.text.strip()

        if "success" in message_text.lower():
            print("   ✓ Найдена зеленая плашка ")

        print(f"\n   ТЕКСТ ЗЕЛЕНОЙ ПЛАШКИ:")
        print("   " + "=" * 40)
        print(f"   {message_text}")
        print("   " + "=" * 40)

        # === ШАГ 7: ПРОВЕРКА И СКРИНШОТ ===
        print("\n7. Проверка успешного входа...")
        print(f"   Текущий URL: {driver.current_url}")

        if "secure" in driver.current_url:
            print("   ✓ Успешный вход на защищенную страницу")

        # Скриншот после входа
        driver.save_screenshot("task4_firefox_after_login.png")
        print("   ✓ Скриншот после входа: task4_firefox_after_login.png")

        time.sleep(2)

    except Exception as e:
        print(f"\n✗ ОШИБКА: {e}")

    finally:
        if driver:
            driver.quit()
            print("\n✓ Firefox закрыт")
            print("\n" + "=" * 70)
            print("УПРАЖНЕНИЕ 4 ЗАВЕРШЕНО!")
            print("=" * 70)


def main():
    """Основная функция"""
    print("Упражнение 4 - Firefox")
    print("=" * 70)
    print("Запустите скрипт для авторизации")
    print("-" * 70)

    response = input("Запустить сейчас? (да/нет): ")
    if response.lower() in ['да', 'д', 'yes', 'y']:
        login_form_firefox()


if __name__ == "__main__":
    main()