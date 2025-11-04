# Тесты для получения заказов пользователя.

import allure
from config.api_helper import create_email
from config.api_config import TEST_USER_DATA
from tests.constants import (
    HTTP_STATUS_OK, HTTP_STATUS_UNAUTHORIZED,
    FIELD_SUCCESS, FIELD_ORDERS, FIELD_TOTAL, FIELD_TOTAL_TODAY, FIELD_DATA, FIELD_ID,
    FIELD_INGREDIENTS, FIELD_STATUS, FIELD_NUMBER, FIELD_CREATED_AT, FIELD_UPDATED_AT, FIELD_MESSAGE,
    USER_FIELD_PASSWORD, USER_FIELD_NAME,
    ERROR_UNAUTHORIZED, MIN_INGREDIENTS, EMPTY_LIST
)


@allure.feature("Получение заказов пользователя")
class TestOrderRetrieval:
    # Тесты для эндпоинта получения заказов пользователя.

    @allure.story("Успешное получение заказов")
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_with_auth(self, registered_user_with_order_email):
        # Проверка получения заказов авторизованного пользователя.
        # Логинимся
        self.api.login_user(
            email=registered_user_with_order_email,
            password=TEST_USER_DATA["password"]
        )
        
        # Получаем заказы пользователя
        response = self.api.get_user_orders()
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_OK, f"Ожидался код {HTTP_STATUS_OK}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is True, f"Поле {FIELD_SUCCESS} должно быть True"
        assert FIELD_ORDERS in response_data, f"В ответе должно быть поле {FIELD_ORDERS}"
        assert FIELD_TOTAL in response_data, f"В ответе должно быть поле {FIELD_TOTAL}"
        assert FIELD_TOTAL_TODAY in response_data, f"В ответе должно быть поле {FIELD_TOTAL_TODAY}"
        
        # Проверяем структуру заказов
        orders = response_data[FIELD_ORDERS]
        assert isinstance(orders, list), "Заказы должны быть списком"
        
        if orders:  # Если есть заказы
            order = orders[0]
            assert FIELD_INGREDIENTS in order, f"В заказе должно быть поле {FIELD_INGREDIENTS}"
            assert FIELD_ID in order, f"В заказе должно быть поле {FIELD_ID}"
            assert FIELD_STATUS in order, f"В заказе должно быть поле {FIELD_STATUS}"
            assert FIELD_NUMBER in order, f"В заказе должно быть поле {FIELD_NUMBER}"
            assert FIELD_CREATED_AT in order, f"В заказе должно быть поле {FIELD_CREATED_AT}"
            assert FIELD_UPDATED_AT in order, f"В заказе должно быть поле {FIELD_UPDATED_AT}"
            
            # Проверяем типы полей
            assert isinstance(order[FIELD_INGREDIENTS], list), "Ингредиенты должны быть списком"
            assert isinstance(order[FIELD_NUMBER], int), "Номер заказа должен быть числом"
            assert isinstance(response_data[FIELD_TOTAL], int), "Общее количество заказов должно быть числом"
            assert isinstance(response_data[FIELD_TOTAL_TODAY], int), "Количество заказов за день должно быть числом"

    @allure.story("Ошибка без авторизации")
    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_without_auth(self):
        # Проверка ошибки при получении заказов без авторизации.
        # Не логинимся, пытаемся получить заказы
        response = self.api.get_user_orders()
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_UNAUTHORIZED, f"Ожидался код {HTTP_STATUS_UNAUTHORIZED}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is False, f"Поле {FIELD_SUCCESS} должно быть False"
        assert FIELD_MESSAGE in response_data, f"В ответе должно быть поле {FIELD_MESSAGE}"
        assert response_data[FIELD_MESSAGE] == ERROR_UNAUTHORIZED, "Сообщение об ошибке не соответствует ожидаемому"

    @allure.story("Получение пустого списка заказов")
    @allure.title("Получение заказов пользователя без заказов")
    def test_get_user_orders_empty(self):
        # Проверка получения заказов пользователя без заказов.
        # Создаем пользователя без заказов
        unique_email = create_email()
        self.api.register_user(
            email=unique_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD],
            name=TEST_USER_DATA[USER_FIELD_NAME]
        )
        self.api.clear_auth()
        
        # Логинимся
        self.api.login_user(
            email=unique_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD]
        )
        
        # Получаем заказы пользователя
        response = self.api.get_user_orders()
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_OK, f"Ожидался код {HTTP_STATUS_OK}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is True, f"Поле {FIELD_SUCCESS} должно быть True"
        assert FIELD_ORDERS in response_data, f"В ответе должно быть поле {FIELD_ORDERS}"
        assert FIELD_TOTAL in response_data, f"В ответе должно быть поле {FIELD_TOTAL}"
        assert FIELD_TOTAL_TODAY in response_data, f"В ответе должно быть поле {FIELD_TOTAL_TODAY}"
        
        # Проверяем, что список заказов пустой
        orders = response_data[FIELD_ORDERS]
        assert isinstance(orders, list), "Заказы должны быть списком"
        assert len(orders) == len(EMPTY_LIST), "Список заказов должен быть пустым"
        # total может быть больше 0 из-за других пользователей в системе
        assert response_data[FIELD_TOTAL] >= 0, "Общее количество заказов должно быть неотрицательным"
        assert response_data[FIELD_TOTAL_TODAY] >= 0, "Количество заказов за день должно быть неотрицательным"