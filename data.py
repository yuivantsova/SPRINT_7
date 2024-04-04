class Data:
    color = ['BLACK']

class TextMessage:
    ERROR_CONFLICT_CREATE_COURIER = 'Этот логин уже используется. Попробуйте другой.'
    ERROR_BAD_REQUEST_CREATE_COURIER = "Недостаточно данных для создания учетной записи"
    ERROR_BAD_REQUEST_LOG_COURIER = 'Недостаточно данных для входа'
    ERROR_NOT_FOUND_LOG_COURIER = 'Учетная запись не найдена'
    ERROR_NOT_FOUND_DELETE_COURIER = 'Курьера с таким id нет.'
    ERROR_BAD_REQUEST_DELETE_COURIER = 'Недостаточно данных для удаления курьера'
    ERROR_BAD_REQUEST_ACCEPT_ORDER_WITHOUT_ID = 'Недостаточно данных для поиска'
    ERROR_NOT_FOUND_COURIER_ACCEPT_ORDER = 'Курьера с таким id не существует'
    ERROR_NOT_FOUND_ORDER_ACCEPT_ORDER = 'Заказа с таким id не существует'
    ERROR_BAD_REQUEST_GET_ORDER_BY_TRACK = 'Недостаточно данных для поиска'
    ERROR_NOT_FOUND_GET_ORDER_BY_TRACK = 'Заказ не найден'