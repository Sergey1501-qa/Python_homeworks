from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def minimal_rename_button():

    edge_options = Options()
    driver = webdriver.Edge(options=edge_options)

    try:
        # 1. Перейдите на сайт
        driver.get("http://uitestingplayground.com/textinput")

        # 2. Укажите в поле ввода текст SkyPro
        input_field = driver.find_element(By.ID, "newButtonName")
        input_field.clear()
        input_field.send_keys("SkyPro")

        # 3. Нажмите на синюю кнопку
        button = driver.find_element(By.ID, "updatingButton")
        button.click()

        # Ожидаем обновления текста кнопки
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.text_to_be_present_in_element((By.ID, "updatingButton"), "SkyPro")
        )

        # 4. Получите текст кнопки и выведите в консоль
        updated_button = driver.find_element(By.ID, "updatingButton")
        print(updated_button.text)

    finally:
        driver.quit()


if __name__ == "__main__":
    minimal_rename_button()