from selenium import webdriver
from selenium.webdriver.common.by import By
import time

print("Запуск упражнения ...")
print("=" * 50)

# Открываем браузер
driver = webdriver.Edge()

# Переходим на страницу
driver.get("http://uitestingplayground.com/dynamicid")
driver.maximize_window()

# Находим кнопку по классу
button = driver.find_element(By.CLASS_NAME, "btn-primary")
print(f"Найдена кнопка: {button.text}")

# Кликаем
button.click()
print("Кнопка нажата!")

# Делаем скриншот
timestamp = time.strftime("%H%M%S")
driver.save_screenshot(f"click_{timestamp}.png")
print(f"Скриншот сохранен")

# Ждем и закрываем
time.sleep(2)
driver.quit()
print("Готово!")