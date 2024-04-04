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
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    login_pass = []

    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

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
