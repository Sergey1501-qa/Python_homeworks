from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def click_button_no_id_chrome():

    print("=" * 60)
    print("УПРАЖНЕНИЕ 2: Клик по кнопке без ID (Chrome)")
    print("=" * 60)

    driver = None
    try:
        # === ШАГ 1: ОТКРЫТЬ GOOGLE CHROME ===
        print("\n1. Открытие Google Chrome...")

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--start-maximized')

        try:
            driver = webdriver.Chrome(options=chrome_options)
            print("   ✓ Chrome открыт")
        except:
            chrome_driver_path = r"C:\WebDriver\chromedriver.exe"
            service = Service(chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            print(f"   ✓ Chrome открыт с драйвером")

        # === ШАГ 2: ПЕРЕЙТИ НА СТРАНИЦУ ===
        print("\n2. Переход на http://uitestingplayground.com/dynamicid...")
        driver.get("http://uitestingplayground.com/dynamicid")
        print("   ✓ Страница загружена")

        # === ШАГ 3: НАЙТИ КНОПКУ ПО КЛАССУ ===
        print("\n3. Поиск кнопки (динамический ID)...")

        wait = WebDriverWait(driver, 10)

        # Ищем по классу (ID динамический и меняется)
        blue_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-primary"))
        )

        button_id = blue_button.get_attribute('id')
        print(f"   ✓ Кнопка найдена!")
        print(f"     ID (динамический): {button_id}")
        print(f"     Текст: {blue_button.text}")

        print("\n4. Клик по кнопке...")
        blue_button.click()
        print("   ✓ Кнопка нажата!")

        # Проверяем изменение ID
        time.sleep(1)
        try:
            new_button = driver.find_element(By.CSS_SELECTOR, "button.btn-primary")
            new_id = new_button.get_attribute('id')
            if new_id != button_id:
                print(f"   ✓ ID изменился: {new_id}")
        except:
            pass

        # === ШАГ 4: СКРИНШОТ ===
        print("\n5. Сохранение скриншота...")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_file = f"task2_chrome_{timestamp}.png"
        driver.save_screenshot(screenshot_file)
        print(f"   ✓ Скриншот: {screenshot_file}")

        time.sleep(2)

    except Exception as e:
        print(f"\n✗ ОШИБКА: {e}")

    finally:
        if driver:
            driver.quit()
            print("\n✓ Chrome закрыт")


def main():
    """Основная функция"""
    print(" Упражнение 2 - Chrome")
    print("=" * 60)
    print("Запустите этот скрипт 3 раза вручную!")
    print("-" * 60)

    response = input("Запустить сейчас? (да/нет): ")
    if response.lower() in ['да', 'д', 'yes', 'y']:
        click_button_no_id_chrome()
        print("\n✓ Запуск 1 завершен. Запустите еще 2 раза!")


if __name__ == "__main__":
    main()