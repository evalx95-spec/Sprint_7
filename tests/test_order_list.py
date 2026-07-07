import allure
import requests
from ..urls import Urls

@allure.feature('Список заказов')
class TestOrdersList:

    @allure.title('Проверка, что тело ответа возвращается список заказов')
    def test_orders_list_returns_list(self):
        response = requests.get(f'{Urls.BASE_URL+Urls.ORDERS}')

        assert response.status_code == 200
        response_json = response.json()
        assert 'orders' in response_json
        assert isinstance(response_json['orders'], list)
