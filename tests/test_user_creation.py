# Тесты для создания пользователя.

import pytest
import allure
from config.api_helper import create_email
from config.api_config import TEST_USER_DATA
from tests.constants import (
    HTTP_STATUS_OK, HTTP_STATUS_FORBIDDEN,
    FIELD_SUCCESS, FIELD_USER, FIELD_ACCESS_TOKEN, FIELD_REFRESH_TOKEN, FIELD_MESSAGE,
    USER_FIELD_EMAIL, USER_FIELD_PASSWORD, USER_FIELD_NAME, FIELDS,
    ERROR_USER_ALREADY_EXISTS, ERROR_REQUIRED_FIELDS
)


@allure.feature("Создание пользователя")
class TestUserCreation:
    # Тесты для эндпоинта создания пользователя.

    @allure.story("Успешное создание пользователя")
    @allure.title("Создать уникального пользователя")
    def test_create_unique_user(self):
        # Проверка создания пользователя с уникальными данными.
        unique_email = create_email()
        
        response = self.api.register_user(
            email=unique_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD],
            name=TEST_USER_DATA[USER_FIELD_NAME]
        )
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_OK, f"Ожидался код {HTTP_STATUS_OK}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is True, f"Поле {FIELD_SUCCESS} должно быть True"
        assert FIELD_USER in response_data, f"В ответе должно быть поле {FIELD_USER}"
        assert FIELD_ACCESS_TOKEN in response_data, f"В ответе должен быть {FIELD_ACCESS_TOKEN}"
        assert FIELD_REFRESH_TOKEN in response_data, f"В ответе должен быть {FIELD_REFRESH_TOKEN}"
        
        user_data = response_data[FIELD_USER]
        assert user_data[USER_FIELD_EMAIL] == unique_email, "Email в ответе не соответствует переданному"
        assert user_data[USER_FIELD_NAME] == TEST_USER_DATA[USER_FIELD_NAME], "Имя в ответе не соответствует переданному"

    @allure.story("Ошибка при создании существующего пользователя")
    @allure.title("Создать пользователя, который уже зарегистрирован")
    def test_create_existing_user(self):
        # Проверка ошибки при создании уже существующего пользователя.
        # Сначала создаем пользователя
        unique_email = create_email()
        self.api.register_user(
            email=unique_email,
            password=TEST_USER_DATA["password"],
            name=TEST_USER_DATA["name"]
        )
        
        # Пытаемся создать пользователя с тем же email
        response = self.api.register_user(
            email=unique_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD],
            name=TEST_USER_DATA[USER_FIELD_NAME]
        )
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_FORBIDDEN, f"Ожидался код {HTTP_STATUS_FORBIDDEN}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is False, f"Поле {FIELD_SUCCESS} должно быть False"
        assert FIELD_MESSAGE in response_data, f"В ответе должно быть поле {FIELD_MESSAGE}"
        assert response_data[FIELD_MESSAGE] == ERROR_USER_ALREADY_EXISTS, "Сообщение об ошибке не соответствует ожидаемому"

    @allure.story("Ошибка при неполных данных")
    @allure.title("Создать пользователя и не заполнить одно из обязательных полей")
    @pytest.mark.parametrize("missing_field", FIELDS)
    def test_create_user_missing_field(self, missing_field):
        # Проверка ошибки при создании пользователя без обязательного поля.
        unique_email = create_email()
        
        # Подготавливаем данные без одного поля
        user_data = {
            USER_FIELD_EMAIL: unique_email,
            USER_FIELD_PASSWORD: TEST_USER_DATA[USER_FIELD_PASSWORD],
            USER_FIELD_NAME: TEST_USER_DATA[USER_FIELD_NAME]
        }
        del user_data[missing_field]
        
        response = self.api.register_user(**user_data)
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_FORBIDDEN, f"Ожидался код {HTTP_STATUS_FORBIDDEN}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is False, f"Поле {FIELD_SUCCESS} должно быть False"
        assert FIELD_MESSAGE in response_data, f"В ответе должно быть поле {FIELD_MESSAGE}"
        assert response_data[FIELD_MESSAGE] == ERROR_REQUIRED_FIELDS, "Сообщение об ошибке не соответствует ожидаемому"
