class Smartphone:

    def __init__(self, brand, model, phone_number):

        self.brand = brand
        self.model = model
        self.phone_number = phone_number

    def get_info(self):

        return f"{self.brand} - {self.model}. {self.phone_number}"

    def __str__(self):
        return self.get_info()

if __name__ == "__main__":

    #Тестовый смартфон
    test_phone = Smartphone("Apple", "iPhone 14", "+79222222222")

    print("Тестовый смартфон:")
    print(test_phone.get_info())
    print(f"Марка: {test_phone.brand}")
    print(f"Модель: {test_phone.model}")
    print(f"Номер: {test_phone.phone_number}")