import math

def square(side):

    area = side * side
    if not isinstance(side, int):
        area = math.ceil(area)
    return area

# Тест 1
side1 = 5
result1 = square(side1)
print(f"Сторона: {side1}, Площадь: {result1}")

# Тест 2
side2 = 3.5
result2 = square(side2)
print(f"Сторона: {side2}, Площадь: {result2}")

# Тест 3
side3 = 2.1
result3 = square(side3)
print(f"Сторона: {side3}, Площадь: {result3}")

# Тест 4
side4 = 4
result4 = square(side4)
print(f"Сторона: {side4}, Площадь: {result4}")

# Тест 5
side5 = 0.5
result5 = square(side5)
print(f"Сторона: {side5}, Площадь: {result5}")