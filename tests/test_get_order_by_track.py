import allure
import pytest

from helpers import *
from data import *

class TestGetOrderByTrack:

    @allure.title('Получение заказа по track')
    def test_get_order_by_track(self):
        track = create_order(Data.color).json()['track']
        response_get = get_order_id(track)
        assert response_get.status_code == 200 and response_get.json()['order']

    @allure.title('Получение заказа без track и несуществующим track')
    @pytest.mark.parametrize('track, status_code, message',
                             [('', 400, TextMessage.ERROR_BAD_REQUEST_GET_ORDER_BY_TRACK),
                             (generator_int(), 404, TextMessage.ERROR_NOT_FOUND_GET_ORDER_BY_TRACK)],
                             ids=['without_track', 'not_valid_track'])
    def test_not_get_order(self, track, status_code, message):
        response_get = get_order_id(track)
        assert response_get.status_code == status_code and response_get.json()['message'] == message
