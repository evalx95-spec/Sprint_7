import allure
import pytest
import requests
from ..api_helpers import *
from ..helpers import *
from ..data import ERROR_MESSAGES, CORRECT_LOGIN, CORRECT_PASSWORD
from ..urls import Urls


@allure.feature('Логин курьера')
class TestLoginCourier:

    @allure.title('Проверка, что курьер может авторизоваться')
    def test_login_courier_success(self, created_courier):
        response = requests.post(
            f'{Urls.BASE_URL+Urls.LOGIN}',
            data={"login": created_courier["login"], "password": created_courier["password"]}
        )

        assert response.status_code == 200
        assert 'id' in response.json()

    @allure.title('Проверка, что для авторизации нужно передать все обязательные поля(отсутствует логиин)')
    def test_login_missing_login(self, created_courier):
        response = requests.post(
            f'{Urls.BASE_URL+Urls.LOGIN}',
            data={"login": "", "password": created_courier["password"]}
        )

        assert response.status_code == 400
        assert ERROR_MESSAGES['missing_login_or_password'] in response.text

    @allure.title('Проверка, что для авторизации нужно передать все обязательные поля(отсутствуе пароль)')
    def test_login_missing_password(self, created_courier):
        response = requests.post(
            f'{Urls.BASE_URL+Urls.LOGIN}',
            data={"login": created_courier["login"], "password": ""}
        )

        assert response.status_code == 400
        assert ERROR_MESSAGES['missing_login_or_password'] in response.text

    @allure.title('Проверка, что система вернёт ошибку, если неправильно указать логин')
    def test_login_wrong_login(self, created_courier):
        wrong_login = generate_random_string(10)
        response = requests.post(
            f'{Urls.BASE_URL+Urls.LOGIN}',
            data={"login": wrong_login, "password": created_courier["password"]}
        )

        assert response.status_code == 404
        assert ERROR_MESSAGES['auth_failed'] in response.text

    @allure.title('Проверка, что система вернёт ошибку, если неправильно указать пароль')
    def test_login_wrong_password(self, created_courier):
        wrong_password = generate_random_string(10)
        response = requests.post(
            f'{Urls.BASE_URL+Urls.LOGIN}',
            data={"login": created_courier["login"], "password": wrong_password}
        )

        assert response.status_code == 404
        assert ERROR_MESSAGES['auth_failed'] in response.text

    @allure.title('Проверка, что если авторизоваться под несуществующим пользователем, запрос возвращает ошибку')
    def test_login_nonexistent_user(self):
        login = generate_random_string(10)
        password = generate_random_string(10)

        response = requests.post(
            f'{Urls.BASE_URL+Urls.LOGIN}',
            data={"login": login, "password": password}
        )

        assert response.status_code == 404
        assert ERROR_MESSAGES['auth_failed'] in response.text

    @allure.title('Проверка, что при успешной авторизации возвращается id курьера')
    def test_login_returns_id(self, created_courier):
        response = requests.post(
            f'{Urls.BASE_URL+Urls.LOGIN}',
            data={"login": created_courier["login"], "password": created_courier["password"]}
        )

        assert response.status_code == 200
        assert 'id' in response.json()
        assert isinstance(response.json()['id'], int)