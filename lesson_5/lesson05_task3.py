from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 1. Открыть браузер
driver = webdriver.Edge()

try:
    # 2. Перейти на страницу
    driver.get("http://the-internet.herokuapp.com/inputs")
    driver.maximize_window()

    # 3. Найти поле ввода
    input_field = driver.find_element(By.TAG_NAME, "input")

    # 4. Ввести "Sky"
    input_field.send_keys("Sky")
    print(f"Введено: {input_field.get_attribute('value')}")
    time.sleep(2)

    # 5. Очистить поле
    input_field.clear()
    print(f"После очистки: '{input_field.get_attribute('value')}'")
    time.sleep(2)

    # 6. Ввести "Pro"
    input_field.send_keys("Pro")
    print(f"Финальный текст: {input_field.get_attribute('value')}")

    # Скриншот
    driver.save_screenshot("lesson_task3.png")
    print("Скриншот сохранен")

    time.sleep(2)

finally:
    # 7. Закрыть браузер
    driver.quit()
    print("Браузер закрыт")