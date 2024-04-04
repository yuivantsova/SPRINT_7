import allure
import pytest
from helpers import *


class TestOrder:

    @allure.title('Проверка создания заказа с передачей разных цветов самоката')
    @pytest.mark.parametrize('color', [(["BLACK"]),
                                       (["GREY"]),
                                       (["GREY", "BLACK"]),
                                       ([''])],
                             ids=['color_black', 'color_grey', 'color_grey_and_black', 'without_color'])
    def test_create_order(self, color):
        response_create = create_order(color)
        assert response_create.status_code == 201 and 'track' in response_create.text

    @allure.title('Проверка на получения списка заказов') # нужно ли тут проверить заказ по курьерам
    def test_get_list_order(self):
        response_get = get_list_order()
        assert response_get.json()['orders']
