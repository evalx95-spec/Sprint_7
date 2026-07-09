import pytest
import requests
from ..api_helpers import delete_courier_by_id
from ..helpers import generate_courier_data
from ..urls import Urls


@pytest.fixture(scope='function')
def create_and_delete_courier():
    
    courier_data = {}
    yield courier_data
    
    # Удаление курьера после теста
    if 'login' in courier_data and 'password' in courier_data:
        auth_response = requests.post(
            f'{Urls.BASE_URL}{Urls.LOGIN}',
            data={"login": courier_data['login'], "password": courier_data['password']}
        )
        if auth_response.status_code == 200:
            courier_id = auth_response.json().get('id')
            if courier_id:
                delete_courier_by_id(courier_id)


@pytest.fixture(scope='function')
def existing_courier():
    """
    Фикстура для создания существующего курьера перед тестом на дубликат.
    """
    login, password, first_name = generate_courier_data()
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }
    response = requests.post(f'{Urls.BASE_URL}{Urls.COURIER}', data=payload)
    assert response.status_code == 201
    
    yield {"login": login, "password": password, "first_name": first_name}
    
    # Удаление курьера после теста
    auth_response = requests.post(
        f'{Urls.BASE_URL}{Urls.LOGIN}',
        data={"login": login, "password": password}
    )
    if auth_response.status_code == 200:
        courier_id = auth_response.json().get('id')
        if courier_id:
            delete_courier_by_id(courier_id)