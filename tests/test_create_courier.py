import allure
import pytest
import requests
from ..api_helpers import delete_courier_by_id
from ..helpers import generate_courier_data, generate_random_string
from ..data import ERROR_MESSAGES
from ..urls import Urls


@allure.feature('Создание курьера')
class TestCreateCourier:

    @allure.title('Проверка успешного создания курьера')
    def test_create_courier_success(self):
        login, password, first_name = generate_courier_data()
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }

        response = requests.post(f'{Urls.BASE_URL}{Urls.COURIER}', data=payload)
        assert response.status_code == 201
        assert response.json() == {'ok': True}

    @allure.title('Проверка ошибки при создании курьера с существующим логином')
    @pytest.fixture(scope='function')
    def existing_courier(self):
        
        login, password, first_name = generate_courier_data()
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        requests.post(f'{Urls.BASE_URL}{Urls.COURIER}', data=payload)
        yield {"login": login, "password": password, "first_name": first_name}
        
        auth_response = requests.post(
            f'{Urls.BASE_URL}{Urls.LOGIN}',
            data={"login": login, "password": password}
        )
        if auth_response.status_code == 200:
            courier_id = auth_response.json().get('id')
            if courier_id:
                delete_courier_by_id(courier_id)

    def test_create_duplicate_courier(self, existing_courier):
        payload = {
            "login": existing_courier['login'],
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        response = requests.post(f'{Urls.BASE_URL}{Urls.COURIER}', data=payload)

        assert response.status_code == 409
        response_json = response.json()
        assert 'message' in response_json and ERROR_MESSAGES['login_already_exists'] in response_json['message']

    @allure.title('Проверка ошибки при отсутствии обязательных полей')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_fields(self, missing_field):
        login, password, first_name = generate_courier_data()
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        del payload[missing_field]

        response = requests.post(f'{Urls.BASE_URL}{Urls.COURIER}', data=payload)
        assert response.status_code == 400
        response_json = response.json()
        assert 'message' in response_json and ERROR_MESSAGES['missing_fields'] in response_json['message']