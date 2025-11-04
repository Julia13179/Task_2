# Фикстуры для тестов API.

import pytest
from config.api_helper import APIHelper, create_email
from config.api_config import TEST_USER_DATA
from tests.constants import (
    USER_FIELD_PASSWORD, USER_FIELD_NAME,
    HTTP_STATUS_OK, FIELD_SUCCESS, FIELD_DATA, FIELD_ID, MIN_INGREDIENTS
)


@pytest.fixture(autouse=True)
def setup(request):
    # Настройка перед каждым тестом.
    api = APIHelper()
    if request.cls:
        request.cls.api = api
    yield api
    # Очистка после теста
    api.clear_auth()


@pytest.fixture
def registered_user_email(setup):
    # Фикстура для создания зарегистрированного пользователя.
    unique_email = create_email()
    setup.register_user(
        email=unique_email,
        password=TEST_USER_DATA[USER_FIELD_PASSWORD],
        name=TEST_USER_DATA[USER_FIELD_NAME]
    )
    setup.clear_auth()
    return unique_email


def _create_user_with_order(api):
    # Создание пользователя с заказом.
    unique_email = create_email()
    api.register_user(
        email=unique_email,
        password=TEST_USER_DATA[USER_FIELD_PASSWORD],
        name=TEST_USER_DATA[USER_FIELD_NAME]
    )
    api.clear_auth()
    
    # Логинимся и создаем заказ
    api.login_user(
        email=unique_email,
        password=TEST_USER_DATA[USER_FIELD_PASSWORD]
    )
    
    # Получаем список доступных ингредиентов
    ingredients_response = api.get_ingredients()
    if ingredients_response.status_code == HTTP_STATUS_OK:
        ingredients_data = ingredients_response.json()
        if ingredients_data[FIELD_SUCCESS] and len(ingredients_data[FIELD_DATA]) >= MIN_INGREDIENTS:
            ingredient_ids = [ingredients_data[FIELD_DATA][0][FIELD_ID], ingredients_data[FIELD_DATA][1][FIELD_ID]]
            api.create_order(ingredient_ids)
    
    api.clear_auth()
    return unique_email


@pytest.fixture
def registered_user_with_order_email(setup):
    # Фикстура для создания зарегистрированного пользователя с заказом.
    return _create_user_with_order(setup)

