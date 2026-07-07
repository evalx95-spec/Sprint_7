import allure
import pytest
import requests
from ..data import *
from ..urls import Urls
from ..helpers import *
from ..api_helpers import *

@allure.feature('Создание заказа')
class TestCreateOrder:
    
    @allure.title('Проверка, что можно указать один из цветов — BLACK или GREY')
    @pytest.mark.parametrize('color', ['BLACK', 'GREY'])
    def test_create_order_black_or_grey_color(self, color):
        order_data = generate_order_data(color)
        response = requests.post(f'{Urls.BASE_URL+Urls.ORDERS}', json=order_data)
        
        assert response.status_code == 201
        assert 'track' in response.json()
        
        track = response.json()['track']
        cancel_order(track)
    
    @allure.title('Проверка, что можно указать оба цвета')
    def test_create_order_both_colors(self):
        order_data = generate_order_data(['BLACK', 'GREY'])
        response = requests.post(f'{Urls.BASE_URL+Urls.ORDERS}', json=order_data)
        
        assert response.status_code == 201
        assert 'track' in response.json()
        
        track = response.json()['track']
        cancel_order(track)
    
    @allure.title('Проверка, что можно не указывать цвет')
    def test_create_order_no_color(self):
        order_data = generate_order_data()
        if 'color' in order_data:
            del order_data['color']
        
        response = requests.post(f'{Urls.BASE_URL+Urls.ORDERS}', json=order_data)
        
        assert response.status_code == 201
        assert 'track' in response.json()
        
        track = response.json()['track']
        cancel_order(track)
    
    @allure.title('Проверка, что тело ответа содержит track')
    def test_create_order_returns_track(self):
        order_data = generate_order_data(['BLACK'])
        response = requests.post(f'{Urls.BASE_URL+Urls.ORDERS}', json=order_data)
        
        assert response.status_code == 201
        response_json = response.json()
        assert 'track' in response_json
        assert isinstance(response_json['track'], int)
        assert response_json['track'] > 0
        
        track = response_json['track']
        cancel_order(track)
