from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def wait_for_images_with_progress():

    print("Ожидание загрузки изображений с прогресс-баром")
    print("-" * 50)

    edge_options = Options()
    edge_options.add_argument('--start-maximized')

    driver = webdriver.Edge(options=edge_options)

    try:
        driver.get("https://bonigarcia.dev/selenium-webdriver-java/loading-images.html")

        print("Загрузка страницы...")

        # Ожидаем загрузки DOM
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

        print("✓ Страница загружена")
        print("\nОжидание изображений...")

        # Ждем контейнер
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "image-container"))
        )

        # Мониторим загрузку изображений
        max_wait_time = 30
        start_time = time.time()

        while time.time() - start_time < max_wait_time:
            images = container.find_elements(By.TAG_NAME, "img")

            if len(images) >= 4:
                loaded = 0
                for img in images:
                    if driver.execute_script(
                            "return arguments[0].complete && arguments[0].naturalWidth > 0",
                            img
                    ):
                        loaded += 1

                # Прогресс-бар
                progress = int(loaded / len(images) * 40)
                bar = "█" * progress + "░" * (40 - progress)
                print(f"\r  [{bar}] {loaded}/{len(images)} изображений", end="")

                if loaded == len(images):
                    print("\n✓ Все изображения загружены!")
                    break

            time.sleep(0.5)
        else:
            print(f"\n⚠ Таймаут: не все изображения загрузились за {max_wait_time} секунд")

        # Получаем 3-ю картинку
        images = container.find_elements(By.TAG_NAME, "img")
        if len(images) >= 3:
            third_src = images[2].get_attribute('src')

            print("\n" + "=" * 60)
            print("SRC 3-й картинки:")
            print("=" * 60)
            print(third_src)
            print("=" * 60)

            # Проверка
            if third_src and third_src.strip():
                print(f"\n✓ Успешно получен src ({len(third_src)} символов)")
            else:
                print(f"\n⚠ Src пустой или не содержит данных")
        else:
            print(f"\n✗ Ошибка: нужно минимум 3 изображения, найдено {len(images)}")

        # Скриншот
        driver.save_screenshot("progress_result.png")
        print(f"\n✓ Скриншот сохранен: progress_result.png")

    except Exception as e:
        print(f"\n✗ Ошибка: {e}")
    finally:
        driver.quit()
        print("\n✓ Браузер закрыт")


if __name__ == "__main__":
    wait_for_images_with_progress()