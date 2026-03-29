from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def input_field_firefox():

    print("=" * 60)
    print("УПРАЖНЕНИЕ 3: Работа с полем ввода (FireFox)")
    print("=" * 60)

    driver = None
    try:
        # === ШАГ 1: ОТКРЫТЬ MOZILLA FIREFOX ===
        print("\n1. Открытие браузера Mozilla Firefox...")

        # Настройка опций Firefox
        firefox_options = Options()
        firefox_options.add_argument('--start-maximized')

        try:
            # Автоматическое обнаружение драйвера
            driver = webdriver.Firefox(options=firefox_options)
            print("   ✓ Firefox успешно открыт")
        except Exception as e:
            print(f"   ✗ Ошибка: {e}")
            print("   Попытка ручной настройки...")

            # Укажите путь к geckodriver.exe
            firefox_driver_path = r"C:\WebDriver\geckodriver.exe"
            service = Service(firefox_driver_path)
            driver = webdriver.Firefox(service=service, options=firefox_options)
            print(f"   ✓ Firefox открыт с драйвером: {firefox_driver_path}")

        # === ШАГ 2: ПЕРЕЙТИ НА СТРАНИЦУ ===
        print("\n2. Переход на http://the-internet.herokuapp.com/inputs...")
        driver.get("http://the-internet.herokuapp.com/inputs")
        print("   ✓ Страница загружена")

        # Ждем загрузки
        wait = WebDriverWait(driver, 10)

        # === ШАГ 3: НАЙТИ ПОЛЕ ВВОДА ===
        print("\n3. Поиск поля ввода...")

        # Находим поле ввода
        input_field = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "input"))
        )

        print(f"   ✓ Поле найдено")
        print(f"     Тип: {input_field.get_attribute('type')}")
        print(f"     Placeholder: {input_field.get_attribute('placeholder')}")

        # === ШАГ 4: ВВЕСТИ "Sky" ===
        print("\n4. Ввод текста 'Sky'...")
        input_field.send_keys("Sky")
        print(f"   ✓ Введено: '{input_field.get_attribute('value')}'")

        time.sleep(1)

        # === ШАГ 5: ОЧИСТИТЬ ПОЛЕ ===
        print("\n5. Очистка поля...")
        input_field.clear()
        cleared = input_field.get_attribute('value')
        print(f"   ✓ После очистки: '{cleared}'")

        time.sleep(1)

        # === ШАГ 6: ВВЕСТИ "Pro" ===
        print("\n6. Ввод текста 'Pro'...")
        input_field.send_keys("Pro")
        final = input_field.get_attribute('value')
        print(f"   ✓ Финальный текст: '{final}'")

        # === ШАГ 7: СКРИНШОТ ===
        print("\n7. Сохранение скриншота...")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_file = f"task3_firefox_{timestamp}.png"
        driver.save_screenshot(screenshot_file)
        print(f"   ✓ Скриншот: {screenshot_file}")

        time.sleep(2)

    except Exception as e:
        print(f"\n✗ ОШИБКА: {e}")

    finally:
        if driver:
            driver.quit()
            print("\n✓ Firefox закрыт")


def main():
    """Основная функция"""
    print("Упражнение 3 - Firefox")
    print("=" * 60)
    print("Запустите скрипт для выполнения упражнения")
    print("-" * 60)

    response = input("Запустить сейчас? (да/нет): ")
    if response.lower() in ['да', 'д', 'yes', 'y']:
        input_field_firefox()
        print("\n✓ Упражнение 3 завершено!")


if __name__ == "__main__":
    main()