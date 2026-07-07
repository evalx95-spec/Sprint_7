import pytest
import requests
from .helpers import *
from .urls import Urls
from .api_helpers import *

@pytest.fixture
def created_courier():
    login, password, first_name = register_new_courier_and_return_login_password()
    if not login:
        pytest.fail("Не удалось создать курьера")

    yield {"login": login, "password": password, "first_name": first_name}

    delete_courier(login, password)