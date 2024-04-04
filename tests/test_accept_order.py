import json
import pytest
from conftest import *
import allure
from data import *
from helpers import *


class TestAcceptOrder:

    @allure.title('курьер принял заказ')
    def test_accept_order(self, register_new_courier_and_return_login_password):
        payload = {
            'login': register_new_courier_and_return_login_password[0],
            'password': register_new_courier_and_return_login_password[1]
        }
        user_id = login_courier(payload).json()['id']
        track = create_order(Data.color).json()['track']
        id_order = get_order_id(track).json()['order']['id']
        response_accept = accept_order(id_order, user_id)
        assert (response_accept.status_code == 200 and
                response_accept.json()['ok'] == True)

    @allure.title('Принять заказ без id курьера')
    def test_no_accept_order_without_id_courier(self):
        track = create_order(Data.color).json()['track']
        id_order = get_order_id(track).json()['order']['id']
        response_accept = accept_order(id_order, '')
        assert (response_accept.status_code == 400 and
                response_accept.json()['message'] == TextMessage.ERROR_BAD_REQUEST_ACCEPT_ORDER_WITHOUT_ID)

    @allure.title('Принять заказ без id заказа')
    def test_no_accept_order_without_id_order(self, register_new_courier_and_return_login_password):
        payload = {
            'login': register_new_courier_and_return_login_password[0],
            'password': register_new_courier_and_return_login_password[1]
        }
        user_id = login_courier(payload).json()['id']
        response_accept = accept_order('', user_id)
        assert (response_accept.status_code == 400 and
                response_accept.json()['message'] == TextMessage.ERROR_BAD_REQUEST_ACCEPT_ORDER_WITHOUT_ID) # Ответ не соотвествует документации

    @allure.title('Принять заказ с неправильным id курьера')
    def test_no_accept_no_valid_id_courier(self, register_new_courier_and_return_login_password):
        payload = {
            'login': register_new_courier_and_return_login_password[0],
            'password': register_new_courier_and_return_login_password[1]
        }
        login_courier(payload)
        track = create_order(Data.color).json()['track']
        id_order = get_order_id(track).json()['order']['id']
        response_accept = accept_order(id_order, generator_int())
        assert (response_accept.status_code == 404 and
                response_accept.json()['message'] == TextMessage.ERROR_NOT_FOUND_COURIER_ACCEPT_ORDER)

    @allure.title('Принять заказ с неправильным id заказа')
    def test_no_accept_no_valid_id_order(self, register_new_courier_and_return_login_password):
        payload = {
            'login': register_new_courier_and_return_login_password[0],
            'password': register_new_courier_and_return_login_password[1]
        }
        user_id = login_courier(payload).json()['id']
        create_order(Data.color)
        response_accept = accept_order(generator_int(), user_id)
        assert (response_accept.status_code == 404 and
                response_accept.json()['message'] == TextMessage.ERROR_NOT_FOUND_ORDER_ACCEPT_ORDER)
