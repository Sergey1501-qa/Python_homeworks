from address import Address


class Mailing:

    def __init__(self, to_address, from_address, cost,):

        self.to_address = to_address
        self.from_address = from_address
        self.cost = cost

    def get_mailing_info(self):

        return (f"Отправление из {self.from_address.get_formatted_for_mailing()} "
                f"в {self.to_address.get_formatted_for_mailing()}. "
                f"Стоимость {self.cost} рублей.")

    def __str__(self):

        return self.get_mailing_info()

if __name__ == "__main__":

    # адреса
    from_addr = Address("101000", "Москва", "Арбат", "15", "3")
    to_addr = Address("190000", "Санкт-Петербург", "Невский проспект", "25", "10")

    # почтовое отправление
    test_mailing = Mailing(
        to_address=to_addr,
        from_address=from_addr,
        cost=150,
    )

    print("Тестовое почтовое отправление:")
    print(f"Стоимость: {test_mailing.cost} рублей")
    print(f"Отправитель: {test_mailing.from_address}")
    print(f"Получатель: {test_mailing.to_address}")