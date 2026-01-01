
def is_year_leap(year):
    return year % 4 == 0

#Вариант 1
year = 2024
result = is_year_leap(year)
print(f"год {year}: {result}")

# Вариант 2
year = 2023
print(f"год {year}: {is_year_leap(year)}")