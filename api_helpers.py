import allure
import requests
from .urls import Urls
from .helpers import generate_random_string

@allure.step('Генерация payload для регистрации курьера')
def generate_courier_payload():
    """Генерирует данные для регистрации курьера"""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    return payload

@allure.step('Регистрация нового курьера')
def register_new_courier(payload):
    """Регистрирует курьера и возвращает данные для входа"""
    response = requests.post(f'{Urls.BASE_URL+Urls.COURIER}', data=payload)
    
    if response.status_code == 201:
        return {
            "login": payload["login"],
            "password": payload["password"],
            "firstName": payload["firstName"]
        }
    return None

@allure.step('Регистрация нового курьера и получение данных для входа')
def register_new_courier_and_return_login_password():
    """Регистрирует курьера и возвращает логин и пароль"""
    payload = generate_courier_payload()
    courier_data = register_new_courier(payload)
    
    if courier_data:
        return courier_data["login"], courier_data["password"], courier_data["firstName"]
    return None, None, None

@allure.step('Логин курьера и получение ID')
def login_courier_and_get_id(login, password):
    """Выполняет вход курьера и возвращает его ID"""
    response = requests.post(
        f'{Urls.BASE_URL+Urls.LOGIN}',
        data={"login": login, "password": password}
    )
    
    if response.status_code == 200:
        return response.json().get('id')
    return None

@allure.step('Удаление курьера по ID')
def delete_courier_by_id(courier_id):
    """Удаляет курьера по его ID"""
    if courier_id:
        response = requests.delete(f'{Urls.BASE_URL+Urls.COURIER}/{courier_id}')
        return response.status_code == 200
    return False

@allure.step('Удаление курьера по логину и паролю')
def delete_courier(login, password):
    """Удаляет курьера, используя логин и пароль для получения ID"""
    courier_id = login_courier_and_get_id(login, password)
    if courier_id:
        return delete_courier_by_id(courier_id)
    return False

@allure.step('Отмена заказа по треку track')
def cancel_order(track):
    """Отменяет заказ по его трек-номеру"""
    response = requests.put(
        f'{Urls.BASE_URL+Urls.CANCEL}',
        json={"track": track}
    )
    return response
