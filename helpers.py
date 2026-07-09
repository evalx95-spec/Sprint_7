import allure
import random
import string
import requests
from .urls import Urls

@allure.step('Генерация случайной строки')
def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

@allure.step('Генерация данных курьера')
def generate_courier_data():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    return login, password, first_name

@allure.step('Генерация данных заказа')
def generate_order_data(color=None):
    first_names = ["Иван", "Петр", "Алексей", "Анна", "Кристина"]
    last_names = ["Иванов", "Петров", "Сидоров", "Трофимова", "Аветова"]
    addresses = ["ул. Гагарина 1", "Бр. Захаровых 8", "ул. Красная Звезда 94"]

    data = {
        "firstName": random.choice(first_names),
        "lastName": random.choice(last_names),
        "address": random.choice(addresses),
        "metroStation": random.randint(1, 20),
        "phone": f"+7{random.randint(9000000000, 9999999999)}",
        "rentTime": random.randint(1, 7),
        "deliveryDate": "2026-07-08",
        "comment": "Тестовый заказ"
    }

    if color:
        data["color"] = color if isinstance(color, list) else [color]

    return data

@allure.step('Генерация данных заказа без указания цвета')
def generate_order_data_without_color():
    """Генерирует данные заказа без поля color"""
    first_names = ["Иван", "Петр", "Алексей", "Анна", "Кристина"]
    last_names = ["Иванов", "Петров", "Сидоров", "Трофимова", "Аветова"]
    addresses = ["ул. Гагарина 1", "Бр. Захаровых 8", "ул. Красная Звезда 94"]

    data = {
        "firstName": random.choice(first_names),
        "lastName": random.choice(last_names),
        "address": random.choice(addresses),
        "metroStation": random.randint(1, 20),
        "phone": f"+7{random.randint(9000000000, 9999999999)}",
        "rentTime": random.randint(1, 7),
        "deliveryDate": "2026-07-08",
        "comment": "Тестовый заказ"
    }

    return data
