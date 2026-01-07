class Address:

    def __init__(self, index, city, street, house, apartment):

        self.index = index
        self.city = city
        self.street = street
        self.house = house
        self.apartment = apartment

    def get_full_address(self):

        return f"{self.index}, {self.city}, {self.street}, {self.house} - {self.apartment}"

    def __str__(self):

        return self.get_full_address()

    def get_formatted_for_mailing(self):

        return f"{self.index}, {self.city}, {self.street}, {self.house} - {self.apartment}"

if __name__ == "__main__":


    # Тестовый адрес
    test_address = Address("123456", "Брянск", "Ленина", "10", "25")

    print("Тестовый адрес:")
    print(f"Индекс: {test_address.index}")
    print(f"Город: {test_address.city}")
    print(f"Улица: {test_address.street}")
    print(f"Дом: {test_address.house}")
    print(f"Квартира: {test_address.apartment}")
    print(f"Полный адрес: {test_address}")