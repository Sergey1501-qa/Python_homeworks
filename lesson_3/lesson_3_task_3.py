from address import Address
from mailing import Mailing

to_address = Address("190000", "Санкт-Петербург", "Невский проспект", "25", "30")
from_address = Address("101000", "Москва", "Тверская", "10", "15")

mailing = Mailing(
    to_address=to_address,
    from_address=from_address,
    cost=250.75,
    track="RU123456789CN"
)
print(mailing.get_mailing_info())