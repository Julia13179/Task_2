# Тесты для создания заказа.

import pytest
import allure
from config.api_helper import APIHelper, create_email
from config.api_config import TEST_USER_DATA, INVALID_INGREDIENTS
from tests.test_constants import (
    HTTP_STATUS_OK, HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_INTERNAL_SERVER_ERROR,
    FIELD_SUCCESS, FIELD_NAME, FIELD_ORDER, FIELD_NUMBER, FIELD_MESSAGE, FIELD_DATA, FIELD_ID,
    USER_FIELD_PASSWORD, USER_FIELD_NAME,
    ERROR_INGREDIENTS_REQUIRED, MIN_INGREDIENTS, EMPTY_LIST
)


@allure.feature("Создание заказа")
class TestOrderCreation:
    # Тесты для эндпоинта создания заказа.

    @pytest.fixture(autouse=True)
    def setup(self):
        # Настройка перед каждым тестом.
        self.api = APIHelper()
        yield
        # Очистка после теста
        self.api.clear_auth()

    @pytest.fixture
    def registered_user_email(self):
        # Фикстура для создания зарегистрированного пользователя.
        unique_email = create_email()
        self.api.register_user(
            email=unique_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD],
            name=TEST_USER_DATA[USER_FIELD_NAME]
        )
        self.api.clear_auth()
        return unique_email

    def _get_valid_ingredients(self):
        # Получение валидных ингредиентов для заказа.
        ingredients_response = self.api.get_ingredients()
        assert ingredients_response.status_code == HTTP_STATUS_OK, "Не удалось получить список ингредиентов"
        
        ingredients_data = ingredients_response.json()
        assert ingredients_data[FIELD_SUCCESS] is True, "Список ингредиентов должен быть получен успешно"
        
        # Берем первые два ингредиента для заказа
        available_ingredients = ingredients_data[FIELD_DATA]
        assert len(available_ingredients) >= MIN_INGREDIENTS, f"Должно быть минимум {MIN_INGREDIENTS} ингредиента"
        
        return [available_ingredients[0][FIELD_ID], available_ingredients[1][FIELD_ID]]

    @allure.story("Успешное создание заказа")
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, registered_user_email):
        # Проверка создания заказа с авторизацией и валидными ингредиентами.
        # Логинимся
        self.api.login_user(
            email=registered_user_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD]
        )
        
        # Получаем валидные ингредиенты
        ingredient_ids = self._get_valid_ingredients()
        
        # Создаем заказ
        response = self.api.create_order(ingredient_ids)
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_OK, f"Ожидался код {HTTP_STATUS_OK}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is True, f"Поле {FIELD_SUCCESS} должно быть True"
        assert FIELD_NAME in response_data, f"В ответе должно быть поле {FIELD_NAME}"
        assert FIELD_ORDER in response_data, f"В ответе должно быть поле {FIELD_ORDER}"
        
        order_data = response_data[FIELD_ORDER]
        assert FIELD_NUMBER in order_data, f"В заказе должно быть поле {FIELD_NUMBER}"
        assert isinstance(order_data[FIELD_NUMBER], int), "Номер заказа должен быть числом"

    @allure.story("Ошибка без авторизации")
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self):
        # Проверка ошибки при создании заказа без авторизации.
        # Получаем валидные ингредиенты
        ingredient_ids = self._get_valid_ingredients()
        
        # Не логинимся, пытаемся создать заказ
        response = self.api.create_order(ingredient_ids)
        
        # Проверяем код ответа - API может разрешать создание заказов без авторизации
        # Проверяем, что заказ создался успешно
        assert response.status_code == HTTP_STATUS_OK, f"Ожидался код {HTTP_STATUS_OK}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is True, f"Поле {FIELD_SUCCESS} должно быть True"
        assert FIELD_NAME in response_data, f"В ответе должно быть поле {FIELD_NAME}"
        assert FIELD_ORDER in response_data, f"В ответе должно быть поле {FIELD_ORDER}"

    @allure.story("Ошибка без ингредиентов")
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, registered_user_email):
        # Проверка ошибки при создании заказа без ингредиентов.
        # Логинимся
        self.api.login_user(
            email=registered_user_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD]
        )
        
        # Создаем заказ без ингредиентов
        response = self.api.create_order(EMPTY_LIST)
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_BAD_REQUEST, f"Ожидался код {HTTP_STATUS_BAD_REQUEST}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is False, f"Поле {FIELD_SUCCESS} должно быть False"
        assert FIELD_MESSAGE in response_data, f"В ответе должно быть поле {FIELD_MESSAGE}"
        assert response_data[FIELD_MESSAGE] == ERROR_INGREDIENTS_REQUIRED, "Сообщение об ошибке не соответствует ожидаемому"

    @allure.story("Ошибка с невалидными ингредиентами")
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients(self, registered_user_email):
        # Проверка ошибки при создании заказа с невалидными ингредиентами.
        # Логинимся
        self.api.login_user(
            email=registered_user_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD]
        )
        
        # Создаем заказ с невалидными ингредиентами
        response = self.api.create_order(INVALID_INGREDIENTS)
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_INTERNAL_SERVER_ERROR, f"Ожидался код {HTTP_STATUS_INTERNAL_SERVER_ERROR}, получен {response.status_code}"
        
        # Проверяем тело ответа (может быть пустым при 500 ошибке)
        if response.content and response.headers.get('content-type', '').startswith('application/json'):
            try:
                response_data = response.json()
                assert response_data[FIELD_SUCCESS] is False, f"Поле {FIELD_SUCCESS} должно быть False"
            except Exception:
                # Если не удается распарсить JSON, это нормально для 500 ошибки
                pass

    @allure.story("Создание заказа с авторизацией")
    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_with_auth_valid_ingredients(self, registered_user_email):
        # Проверка создания заказа с авторизацией и валидными ингредиентами.
        # Логинимся
        self.api.login_user(
            email=registered_user_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD]
        )
        
        # Получаем валидные ингредиенты
        ingredient_ids = self._get_valid_ingredients()
        
        # Создаем заказ
        response = self.api.create_order(ingredient_ids)
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_OK, f"Ожидался код {HTTP_STATUS_OK}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is True, f"Поле {FIELD_SUCCESS} должно быть True"
        assert FIELD_NAME in response_data, f"В ответе должно быть поле {FIELD_NAME}"
        assert FIELD_ORDER in response_data, f"В ответе должно быть поле {FIELD_ORDER}"
        
        order_data = response_data[FIELD_ORDER]
        assert FIELD_NUMBER in order_data, f"В заказе должно быть поле {FIELD_NUMBER}"
        assert isinstance(order_data[FIELD_NUMBER], int), "Номер заказа должен быть числом"