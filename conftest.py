import string
import random

import allure
import pytest
import requests
from endpoint import *
from helpers import *


@allure.step('Создание курьера,регистарция с последующим удалением ')
@pytest.fixture
def register_new_courier_and_return_login_password():

    login_pass = []

    login = generator_str(10)
    password = generator_str(10)
    first_name = generator_str(10)

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = requests.post(f'{URL + CREATE_COURIER}', data=payload)

    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    yield login_pass

    payload = {
        'login': login,
        'password': password
    }
    response_log = requests.post(f'{URL + LOGIN_COURIER}', json=payload)
    user_id = response_log.json()['id']
    delete_courier(user_id)
