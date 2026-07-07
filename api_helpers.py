import requests
from .urls import Urls
from .helpers import *
def register_new_courier_and_return_login_password():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(f'{Urls.BASE_URL+Urls.COURIER}', data=payload)
    if response.status_code == 201:
        return login, password, first_name
    return None, None, None
def delete_courier(login, password):
    response = requests.post(
        f'{Urls.BASE_URL+Urls.LOGIN}',
        data={"login": login, "password": password}
    )
    
    if response.status_code == 200:
        courier_id = response.json().get('id')
        if courier_id:
            requests.delete(f'{Urls.BASE_URL+Urls.COURIER}/{courier_id}')
            return True
    return False
def delete_courier_by_id(courier_id):
    if courier_id:
        requests.delete(f'{Urls.BASE_URL+Urls.COURIER}/{courier_id}')
        return True
    return False

@allure.step('Отмена заказа по треку track')
def cancel_order(track):
    response = requests.put(
        f'{Urls.BASE_URL+Urls.CANCEL}',
        json={"track": track}
    )
    return response
