import allure
import pytest
import requests
from ..api_helpers import delete_courier_by_id, generate_courier_payload
from ..helpers import generate_courier_data, generate_random_string
from ..data import ERROR_MESSAGES
from ..urls import Urls


@allure.feature('Создание курьера')
class TestCreateCourier:

    @allure.title('Проверка успешного создания курьера')
    def test_create_courier_success(self, create_and_delete_courier):
        
        
        assert 'login' in create_and_delete_courier
        assert 'password' in create_and_delete_courier
        assert 'firstName' in create_and_delete_courier
        
        
        auth_response = requests.post(
            f'{Urls.BASE_URL}{Urls.LOGIN}',
            data={
                "login": create_and_delete_courier['login'], 
                "password": create_and_delete_courier['password']
            }
        )
        assert auth_response.status_code == 200
        assert 'id' in auth_response.json()

    @allure.title('Проверка ошибки при создании курьера с существующим логином')
    def test_create_duplicate_courier(self, existing_courier):
        
        payload = {
            "login": existing_courier['login'],
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        with allure.step('Отправка запроса на создание дубликата курьера'):
            response = requests.post(f'{Urls.BASE_URL}{Urls.COURIER}', data=payload)

        with allure.step('Проверка ответа на дубликат'):
            assert response.status_code == 409
            response_json = response.json()
            assert 'message' in response_json 
            assert ERROR_MESSAGES['login_already_exists'] in response_json['message']

    @allure.title('Проверка ошибки при отсутствии обязательных полей')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_fields(self, missing_field):
        
        payload = generate_courier_payload()
        del payload[missing_field]

        with allure.step(f'Отправка запроса без поля {missing_field}'):
            response = requests.post(f'{Urls.BASE_URL}{Urls.COURIER}', data=payload)
        
        with allure.step('Проверка ответа на отсутствующее поле'):
            assert response.status_code == 400
            response_json = response.json()
            assert 'message' in response_json 
            assert ERROR_MESSAGES['missing_fields'] in response_json['message']
            