import json
import allure
import pytest
import requests
import random
import string
from endpoint import *


@allure.step('Получение рандомной строки')
def generator_str(length):
    characters = string.ascii_letters + string.ascii_lowercase
    random_str = ''.join(random.choice(characters) for _ in range(length))
    return random_str


@allure.step('Получение рандомного числа')
def generator_int():
    random_number = random.randint(100000, 9999999)
    return random_number


@allure.title('Создание курьера')
def create_courier(payload):
    response_create = requests.post(f'{URL + CREATE_COURIER}', json=payload)
    return response_create


@allure.step('Регистрация курьера')
def login_courier(payload):
    payload = json.dumps(payload)
    headers = {"Content-type": "application/json"}
    response_login = requests.post(f'{URL + LOGIN_COURIER}', data=payload, headers=headers)
    return response_login


@allure.step('Удаление курьера')
def delete_courier(user_id):
    payload = {
        "id": user_id
    }
    response_delete = requests.delete(f'{URL + CREATE_COURIER}/{user_id}', json=payload)
    return response_delete


@allure.step('Создание заказа')
def create_order(color):
    payload = {
        "firstName": generator_str(5),
        "lastName": generator_str(5),
        "address": f'{generator_str(6), 5}',
        "metroStation": 6,
        "phone": "+79997775544",
        "rentTime": 5,
        "deliveryDate": '2024-03-18',
        "comment": 'Прошу привести через час',
        "color": color
    }
    payload = json.dumps(payload)
    headers = {"Content-type": "application/json"}
    response_create = requests.post(f'{URL + CREATE_AND_GET_ORDER}', data=payload, headers=headers)
    return response_create


@allure.step('Получение списка заказов')
def get_list_order():
    response_get = requests.get(f'{URL+CREATE_AND_GET_ORDER}')
    return response_get


@allure.step('Создание и регистрация курьера')
def create_and_log_courier():
    payload = {
        'login': generator_str(6),
        'password': generator_str(6),
        'name': generator_str(4)
    }
    create_courier(payload)
    response_log = login_courier(payload)
    return response_log


@allure.step('Принять заказ')
def accept_order(track, user_id):
    response = requests.put(f'{URL+ACCEPT_ORDER}/{track}?courierId={user_id}')
    return response


@allure.step('Получить id заказа по track')
def get_order_id(track):
    response = requests.get(f'{URL+GET_ORDER_TRACK}?t={track}')
    return response


