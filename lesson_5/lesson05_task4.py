from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def login_form_exercise():

    print("=" * 70)
    print("Форма авторизации")
    print("=" * 70)

    driver = None
    try:
        # === ШАГ 1: ОТКРЫТЬ БРАУЗЕР MICROSOFT EDGE ===
        print("\n1. Открытие браузера Microsoft Edge...")

        try:
            driver = webdriver.Edge()
            print("   ✓ Браузер успешно открыт")
        except Exception as e:
            print(f"   ✗ Ошибка: {e}")
            print("   Пробую ручную настройку драйвера...")

            edge_driver_path = r"C:\WebDriver\msedgedriver.exe"
            service = Service(edge_driver_path)
            driver = webdriver.Edge(service=service)
            print(f"   ✓ Браузер открыт: {edge_driver_path}")

        # === ШАГ 2: ПЕРЕЙТИ НА СТРАНИЦУ ЛОГИНА ===
        print("\n2. Переход на страницу http://the-internet.herokuapp.com/login...")
        driver.get("http://the-internet.herokuapp.com/login")
        print("   ✓ Страница загружена")

        # Максимизируем окно
        driver.maximize_window()

        # Создаем объект ожидания
        wait = WebDriverWait(driver, 10)

        # === ШАГ 3: НАЙТИ И ЗАПОЛНИТЬ ПОЛЕ USERNAME ===
        print("\n3. Поиск и заполнение поля username...")

        # Находим поле username по ID
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )

        # Вводим логин
        username_field.send_keys("tomsmith")
        entered_username = username_field.get_attribute('value')
        print(f"   ✓ Введен username: '{entered_username}'")

        # === ШАГ 4: НАЙТИ И ЗАПОЛНИТЬ ПОЛЕ PASSWORD ===
        print("\n4. Поиск и заполнение поля password...")

        # Находим поле password по ID
        password_field = driver.find_element(By.ID, "password")

        # Вводим пароль
        password_field.send_keys("SuperSecretPassword!")
        entered_password = password_field.get_attribute('value')
        print(f"   ✓ Введен password: '{'*' * len(entered_password)}'")
        print(f"     (длина пароля: {len(entered_password)} символов)")

        # Делаем скриншот формы перед отправкой
        time.sleep(1)
        driver.save_screenshot("task4_login_form.png")
        print("   ✓ Скриншот формы сохранен: task4_login_form.png")

        # === ШАГ 5: НАЖАТЬ КНОПКУ LOGIN ===
        print("\n5. Поиск и нажатие кнопки Login...")

        # Находим кнопку Login
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        button_text = login_button.text
        print(f"   ✓ Найдена кнопка: '{button_text}'")

        # Нажимаем кнопку
        print("   Нажимаю кнопку Login...")
        login_button.click()
        print("   ✓ Кнопка нажата")

        # Ждем обновление страницы
        time.sleep(2)

        # === ШАГ 6: НАЙТИ И ВЫВЕСТИ ТЕКСТ С ЗЕЛЕНОЙ ПЛАШКИ ===
        print("\n6. Поиск текста с зеленой плашки (успешный вход)...")

        # Ждем появления элемента с сообщением об успехе
        success_message = wait.until(
            EC.presence_of_element_located((By.ID, "flash"))
        )

        # Получаем текст из элемента
        message_text = success_message.text.strip()

        # Проверяем, что это зеленая плашка (успех)
        if "success" in message_text.lower() or "logged" in message_text.lower():
            print("   Найдена зеленая плашка с сообщением об успехе")
        else:
            print("    Найдено сообщение, но возможно не зеленое")

        # Выводим текст сообщения
        print(f"\n   ТЕКСТ СООБЩЕНИЯ:")
        print("   " + "=" * 40)
        print(f"   {message_text}")
        print("   " + "=" * 40)

        # Проверяем цвет плашки
        try:
            message_class = success_message.get_attribute('class')
            print(f"\n   Классы плашки: {message_class}")

            if 'success' in message_class:
                print("   ✓ Подтверждено: это зеленая плашка успеха")
        except:
            pass

        # === ШАГ 7: ПРОВЕРКА УСПЕШНОГО ВХОДА ===
        print("\n7. Проверка успешного входа...")

        # Проверяем текущий URL
        current_url = driver.current_url
        print(f"   Текущий URL: {current_url}")

        if "secure" in current_url.lower():
            print("   Успешный вход на защищенную страницу")

        # Проверяем заголовок страницы
        page_title = driver.title
        print(f"   Заголовок страницы: '{page_title}'")

        # Проверяем наличие кнопки Logout
        try:
            logout_button = driver.find_element(By.CSS_SELECTOR, "a.button.secondary.radius")
            logout_text = logout_button.text
            print(f"   Найдена кнопка выхода: '{logout_text}'")
        except:
            print("   Кнопка выхода не найдена")


        # Делаем скриншот после входа
        time.sleep(1)
        driver.save_screenshot("task4_after_login.png")
        print("   ✓ Скриншот после входа: task4_after_login.png")

        # Выводим время выполнения
        print(f"   Время выполнения: {time.strftime('%H:%M:%S')}")

        # Пауза для визуальной проверки
        print("\n" + "-" * 70)
        print("Демонстрация результата (5 секунд)...")
        print("Проверьте:")
        print("1. Зеленое сообщение об успешном входе")
        print("2. URL содержит 'secure'")
        print("3. Есть кнопка Logout")
        print("-" * 70)
        time.sleep(5)

    except Exception as e:
        print(f"\n✗ ОШИБКА: {e}")
        print("\nВозможные причины:")
        print("1. Сайт недоступен")
        print("2. Неправильные учетные данные")
        print("3. Изменилась структура страницы")
        print("4. Не найден один из элементов")

        # Пробуем сделать скриншот ошибки
        if driver:
            try:
                driver.save_screenshot("task4_error.png")
                print("Скриншот ошибки сохранен: task4_error.png")
            except:
                pass

        input("\nНажмите Enter для продолжения...")

    finally:
        # === ШАГ 9: ЗАКРЫТЬ БРАУЗЕР ===
        print("\n9. Закрытие браузера (метод quit())...")
        if driver:
            driver.quit()
            print("   ✓ Браузер закрыт")

        print("\n" + "=" * 70)
        print("ЗАВЕРШЕНО!")
        print("=" * 70)


def main():

    # Подтверждение запуска
    response = input("\nЗапустить упражнение 4? (да/нет): ")

    if response.lower() in ['да', 'д', 'yes', 'y']:
        login_form_exercise()

        # Инструкция для проверки
        print("\n" + "=" * 70)
        print("СКРИПТ ВЫПОЛНЕН!")
        print("=" * 70)
        print("\nПроверьте созданные файлы:")
        print("1. task4_login_form.png - форма перед отправкой")
        print("2. task4_after_login.png - страница после входа")
        print("=" * 70)

        input("\nНажмите Enter для выхода...")

    else:
        print("Запуск отменен.")
        input("Нажмите Enter для выхода...")


if __name__ == "__main__":
    main()