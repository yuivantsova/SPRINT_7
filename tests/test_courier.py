import json
from conftest import *
import allure
import pytest
from data import *
from helpers import *


class TestCreateCourier:

    @allure.title('Проверка создания курьера')
    def test_create_new_courier(self):
        payload = {
            'login': generator_str(6),
            'password': generator_str(5),
            'name': generator_str(7)
        }
        response_create = create_courier(payload)
        assert response_create.status_code == 201 and response_create.json()['ok'] == True

    @allure.title('Проверка создания курьера с пустыми полями')
    @pytest.mark.parametrize('payload', [({'login': '', 'password': generator_str(5), 'name': generator_str(8)}),
                                         ({'login': generator_str(6), 'password':'', 'name': generator_str(8)}),
                                         ({'login': generator_str(5), 'name': generator_str(8)}),
                                         ({'password': generator_str(7)})],
                                         ids=['empty login', 'empty password', 'without password', 'without login'])
    def test_create_new_courier_not_valid_data(self, payload):
        response_create = create_courier(payload)
        assert (response_create.status_code == 400 and
                response_create.json()['message'] == TextMessage.ERROR_BAD_REQUEST_CREATE_COURIER)

    @allure.title('Проверка создания курьеров с одинаковым login')
    def test_create_double_courier(self):
        payload = {
            'login': generator_str(6),
            'password': generator_str(5),
            'name': generator_str(7)
        }
        create_courier(payload)
        response_create_second = create_courier(payload)
        assert (response_create_second.status_code == 409 and
                response_create_second.json()['message'] == TextMessage.ERROR_CONFLICT_CREATE_COURIER)


class TestLoginCourier:
    @allure.title('Логин курьера')
    def test_login_courier(self, register_new_courier_and_return_login_password):
        payload = {
            'login': register_new_courier_and_return_login_password[0],
            'password': register_new_courier_and_return_login_password[1]
        }
        response_log = login_courier(payload)
        assert response_log.status_code == 200 and 'id' in response_log.text

    @allure.title('Логин курьера с пустым login')
    def test_login_courier_empty_login(self, register_new_courier_and_return_login_password):
        payload = {
            'login': '',
            'password': register_new_courier_and_return_login_password[1]
        }
        response_log = login_courier(payload)
        assert (response_log.status_code == 400 and
                response_log.json()['message'] == TextMessage.ERROR_BAD_REQUEST_LOG_COURIER)

    @allure.title('Логин курьера с пустым password')
    def test_login_courier_empty_password(self, register_new_courier_and_return_login_password):
        payload = {
            'login': register_new_courier_and_return_login_password[0],
            'password': ''
        }
        response_log = login_courier(payload)
        assert (response_log.status_code == 400 and
                response_log.json()['message'] == TextMessage.ERROR_BAD_REQUEST_LOG_COURIER)

    @allure.title('Логин курьера без поля login')
    def test_login_courier_without_login(self, register_new_courier_and_return_login_password):
        payload = {
            'password': register_new_courier_and_return_login_password[1]
        }
        response_log = login_courier(payload)
        assert (response_log.status_code == 400 and
                response_log.json()['message'] == TextMessage.ERROR_BAD_REQUEST_LOG_COURIER)

    @allure.title('Логин курьера без поля password')
    def test_login_courier_without_password(self, register_new_courier_and_return_login_password):
        payload = {
            'login': register_new_courier_and_return_login_password[0]
        }
        response_log = login_courier(payload)
        assert response_log.status_code == 504

    @allure.title('Логин курьера с логином зарегестрированного пользователя и неправильным паролем')
    def test_login_courier_no_valid_password(self, register_new_courier_and_return_login_password):
        payload = {
            "login": register_new_courier_and_return_login_password[0],
            "password": generator_str(5)
        }
        response_log = login_courier(payload)
        assert (response_log.status_code == 404 and
                response_log.json()['message'] == TextMessage.ERROR_NOT_FOUND_LOG_COURIER)

    @allure.title('Логин курьера с паролем от зарегестрированного пользователя и неправильным логином')
    def test_login_courier_no_valid_login(self, register_new_courier_and_return_login_password):
        payload = {
            "login": generator_str(5),
            "password": register_new_courier_and_return_login_password[1]
        }
        response_log = login_courier(payload)
        assert (response_log.status_code == 404 and
                response_log.json()['message'] == TextMessage.ERROR_NOT_FOUND_LOG_COURIER)

    @allure.title('Логин курьера с несуществующими данными')
    def test_login_courier_no_valid_data(self):
        payload = {
            'login': generator_str(5),
            'password': generator_str(6)
        }
        response_log = login_courier(payload)
        assert (response_log.status_code == 404 and
                response_log.json()['message'] == TextMessage.ERROR_NOT_FOUND_LOG_COURIER)


class TestDeleteCourier:

    @allure.title('Удаление курьера')
    def test_delete_courier_true(self):
        response_log = create_and_log_courier().json()['id']
        response_del = delete_courier(response_log)
        assert response_del.status_code == 200 and response_del.json()['ok'] == True

    @allure.title('Удаление курьера с несуществующим id')
    def test_delete_courier_non_existent_(self):
        response_del_repeat = delete_courier(generator_int())
        assert (response_del_repeat.status_code == 404 and
                response_del_repeat.json()['message'] == TextMessage.ERROR_NOT_FOUND_DELETE_COURIER)

    @allure.title('Удаление курьера без id')
    def test_delete_courier_without_id(self):
        response_del = requests.delete(f'{URL+DELETE_COURIER}')
        assert (response_del.status_code == 400 and
                response_del.json()['message'] == TextMessage.ERROR_BAD_REQUEST_DELETE_COURIER)
        # Ответ не соотвествует документации
