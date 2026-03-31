from smartphone import Smartphone


def main():
    print("=== Каталог смартфонов ===")

    catalog = []


    # Смартфон 1
    phone1 = Smartphone("Apple", "iPhone 15 Pro", "+79111234567")
    catalog.append(phone1)
    print(f"Добавлен: {phone1}")

    # Смартфон 2
    phone2 = Smartphone("Samsung", "Galaxy S24", "+79222345678")
    catalog.append(phone2)
    print(f"Добавлен: {phone2}")

    # Смартфон 3
    phone3 = Smartphone("Xiaomi", "Redmi", "+79333456789")
    catalog.append(phone3)
    print(f"Добавлен: {phone3}")

    # Смартфон 4
    phone4 = Smartphone("Google", "Pixel 8", "+79444567890")
    catalog.append(phone4)
    print(f"Добавлен: {phone4}")

    # Смартфон 5
    phone5 = Smartphone("OnePlus", "12", "+79555678901")
    catalog.append(phone5)
    print(f"Добавлен: {phone5}")

    print(f"\nВсего в каталоге: {len(catalog)} смартфонов")

if __name__ == "__main__":
    main()