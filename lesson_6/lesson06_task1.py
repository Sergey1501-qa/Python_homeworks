from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def minimal_edge_ajax():

    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument('--start-maximized')

    driver = webdriver.Edge(options=edge_options)

    try:
        # 1. Перейдите на страницу
        driver.get("http://uitestingplayground.com/ajax")

        # 2. Нажмите на синюю кнопку
        wait = WebDriverWait(driver, 16)
        button = wait.until(EC.element_to_be_clickable((By.ID, "ajaxButton")))
        button.click()

        # 3. Получите текст из зеленой плашки
        # Ждем появления элемента
        success_message = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "bg-success"))
        )

        # 4. Выведите его в консоль
        print(success_message.text.strip())

    finally:
        driver.quit()

if __name__ == "__main__":
    minimal_edge_ajax()