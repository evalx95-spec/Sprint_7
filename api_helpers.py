import allure
import requests
from .urls import Urls
from .helpers import generate_random_string

@allure.step('Генерация payload для регистрации курьера')
def generate_courier_payload():
    
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
    
    payload = generate_courier_payload()
    courier_data = register_new_courier(payload)
    
    if courier_data:
        return courier_data["login"], courier_data["password"], courier_data["firstName"]
    return None, None, None

@allure.step('Логин курьера и получение ID')
def login_courier_and_get_id(login, password):
    
    response = requests.post(
        f'{Urls.BASE_URL+Urls.LOGIN}',
        data={"login": login, "password": password}
    )
    
    if response.status_code == 200:
        return response.json().get('id')
    return None

@allure.step('Удаление курьера по ID')
def delete_courier_by_id(courier_id):
    if courier_id:
        response = requests.delete(f'{Urls.BASE_URL}{Urls.COURIER}/{courier_id}')
        return response.status_code == 200
    return False
@allure.step('Удаление заказа по номеру трека')
def cancel_order(track_number):
    if track_number:
        response = requests.put(
            f'{Urls.BASE_URL}{Urls.ORDERS}/cancel',
            json={"trackId": track_number}
        )
        return response.status_code == 200
    return False
