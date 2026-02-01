from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def click_blue_button_chrome():

    print("=" * 60)
    print("УПРАЖНЕНИЕ 1: Клик по кнопке с CSS-классом (Chrome)")
    print("=" * 60)

    driver = None
    try:
        # === ШАГ 1: ОТКРЫТЬ БРАУЗЕР GOOGLE CHROME ===
        print("\n1. Открытие браузера Google Chrome...")

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--start-maximized')

        try:
            # Автоматическое обнаружение драйвера
            driver = webdriver.Chrome(options=chrome_options)
            print("   ✓ Chrome успешно открыт")
        except Exception as e:
            print(f"   ✗ Ошибка: {e}")
            print("   Попытка ручной настройки...")

            # Укажите путь к chromedriver.exe
            chrome_driver_path = r"C:\WebDriver\chromedriver.exe"
            service = Service(chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print(f"   ✓ Chrome открыт с драйвером: {chrome_driver_path}")

        # === ШАГ 2: ПЕРЕЙТИ НА СТРАНИЦУ ===
        print("\n2. Переход на http://uitestingplayground.com/classattr...")
        driver.get("http://uitestingplayground.com/classattr")
        print("   ✓ Страница загружена")

        # === ШАГ 3: НАЙТИ И КЛИКНУТЬ НА СИНЮЮ КНОПКУ ===
        print("\n3. Поиск синей кнопки по классу 'btn-primary'...")

        wait = WebDriverWait(driver, 10)

        blue_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-primary"))
        )

        # Выводим информацию
        print(f"   ✓ Кнопка найдена!")
        print(f"     Текст: {blue_button.text}")
        print(f"     Класс: {blue_button.get_attribute('class')}")

        print("\n4. Клик по кнопке...")
        blue_button.click()
        print("   ✓ Кнопка нажата!")

        # === ШАГ 4: СОХРАНЕНИЕ СКРИНШОТА ===
        print("\n5. Сохранение скриншота...")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_file = f"task1_chrome_{timestamp}.png"
        driver.save_screenshot(screenshot_file)
        print(f"   ✓ Скриншот: {screenshot_file}")

        # Пауза
        time.sleep(2)

    except Exception as e:
        print(f"\n✗ ОШИБКА: {e}")

    finally:
        if driver:
            driver.quit()
            print("\n✓ Chrome закрыт")


def main():
    """Основная функция"""
    print("Упражнение 1 - Chrome")
    print("=" * 60)
    print("Запустите этот скрипт 3 раза вручную!")
    print("-" * 60)

    response = input("Запустить сейчас? (да/нет): ")
    if response.lower() in ['да', 'д', 'yes', 'y']:
        click_blue_button_chrome()
        print("\n✓ Запуск 1 завершен. Запустите еще 2 раза!")


if __name__ == "__main__":
    main()