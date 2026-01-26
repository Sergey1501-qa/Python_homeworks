from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


def click_blue_button_edge():


    try:
        # 1. Открыть браузер Microsoft Edge
        print("1. Запуск браузера Microsoft Edge...")

        try:
            driver = webdriver.Edge()
        except:

            edge_driver_path = r"C:\WebDriver\msedgedriver.exe"  # Укажите ваш путь
            service = Service(edge_driver_path)
            driver = webdriver.Edge(service=service)


        driver.get("http://uitestingplayground.com/classattr")

        # Увеличиваем окно браузера
        driver.maximize_window()

        # 3. Кликнуть на синюю кнопку
        print("3. Поиск и клик по синей кнопке...")

        # Ждем, пока страница загрузится и кнопка станет кликабельной
        wait = WebDriverWait(driver, 10)

        blue_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary')]"))
        )

        # Кликаем на кнопку
        print("4. Кликаем по кнопке...")
        blue_button.click()
        print("   ✓ Кнопка успешно нажата!")

        # Даем время увидеть результат
        time.sleep(2)

        # 4. Проверяем, появилось ли всплывающее окно (alert)
        print("5. Проверка всплывающих окон...")
        try:
            alert = driver.switch_to.alert
            alert_text = alert.text
            print(f"   Обнаружено всплывающее окно с текстом: '{alert_text}'")
            alert.accept()  # Закрываем всплывающее окно
            print("   ✓ Всплывающее окно закрыто.")
        except:
            print("   Всплывающее окно не обнаружено.")

        # 5. Делаем скриншот для подтверждения
        print("6. Делаем скриншот...")
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = f"lesson05_task1_screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        print(f"   Скриншот сохранен как: {screenshot_path}")

        # Делаем небольшую паузу перед закрытием
        time.sleep(1)

        print("\n✓ Скрипт успешно выполнен!")

    except Exception as e:
        print(f"\n✗ Произошла ошибка: {e}")
        # Выводим детали ошибки
        import traceback
        traceback.print_exc()

    finally:
        # Закрываем браузер
        if 'driver' in locals():
            driver.quit()
            print("Браузер закрыт.")
        print("=" * 60)


def main():

    # Запрашиваем подтверждение у пользователя
    user_input = input("Запустить скрипт? (y/n): ")

    if user_input.lower() == 'y':
        click_blue_button_edge()
    else:
        print("Запуск отменен.")


if __name__ == "__main__":
    main()