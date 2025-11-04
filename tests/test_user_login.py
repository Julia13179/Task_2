# Тесты для логина пользователя.

import pytest
import allure
from config.api_helper import APIHelper, create_email
from config.api_config import TEST_USER_DATA
from tests.test_constants import (
    HTTP_STATUS_OK, HTTP_STATUS_UNAUTHORIZED,
    FIELD_SUCCESS, FIELD_USER, FIELD_ACCESS_TOKEN, FIELD_REFRESH_TOKEN, FIELD_MESSAGE,
    USER_FIELD_EMAIL, USER_FIELD_PASSWORD, USER_FIELD_NAME,
    ERROR_INCORRECT_CREDENTIALS, TEST_EMAILS, TEST_PASSWORDS, INVALID_DESC, MISSING_DESC
)


@allure.feature("Логин пользователя")
class TestUserLogin:
    # Тесты для эндпоинта логина пользователя.

    @pytest.fixture(autouse=True)
    def setup(self):
        # Настройка перед каждым тестом.
        self.api = APIHelper()
        yield
        # Очистка после теста
        self.api.clear_auth()

    @allure.story("Успешный логин")
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self):
        # Проверка успешного логина существующего пользователя.
        # Сначала создаем пользователя
        unique_email = create_email()
        self.api.register_user(
            email=unique_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD],
            name=TEST_USER_DATA[USER_FIELD_NAME]
        )
        
        # Очищаем авторизацию после регистрации
        self.api.clear_auth()
        
        # Логинимся
        response = self.api.login_user(
            email=unique_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD]
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
        
        # Проверяем, что токены сохранились
        assert self.api.access_token is not None, "Access token должен быть сохранен"
        assert self.api.refresh_token is not None, "Refresh token должен быть сохранен"

    @allure.story("Ошибка при неверных данных")
    @allure.title("Логин с неверным логином и паролем")
    @pytest.mark.parametrize("email,password,description", [
        (TEST_EMAILS[0], TEST_USER_DATA["password"], INVALID_DESC[0]),
        (TEST_USER_DATA["email"], TEST_PASSWORDS[1], INVALID_DESC[1]),
        (TEST_EMAILS[0], TEST_PASSWORDS[1], INVALID_DESC[2])
    ])
    def test_login_invalid_credentials(self, email, password, description):
        # Проверка ошибки при логине с неверными данными.
        response = self.api.login_user(email=email, password=password)
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_UNAUTHORIZED, f"Ожидался код {HTTP_STATUS_UNAUTHORIZED}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is False, f"Поле {FIELD_SUCCESS} должно быть False"
        assert FIELD_MESSAGE in response_data, f"В ответе должно быть поле {FIELD_MESSAGE}"
        assert response_data[FIELD_MESSAGE] == ERROR_INCORRECT_CREDENTIALS, "Сообщение об ошибке не соответствует ожидаемому"
        
        # Проверяем, что токены не сохранились
        assert self.api.access_token is None, "Access token не должен быть сохранен при ошибке"
        assert self.api.refresh_token is None, "Refresh token не должен быть сохранен при ошибке"

    @allure.story("Ошибка при неполных данных")
    @allure.title("Логин без обязательных полей")
    @pytest.mark.parametrize("email,password,description", [
        (TEST_EMAILS[2], TEST_USER_DATA["password"], MISSING_DESC[0]),
        (TEST_USER_DATA["email"], TEST_PASSWORDS[2], MISSING_DESC[1]),
        (TEST_EMAILS[2], TEST_PASSWORDS[2], MISSING_DESC[2])
    ])
    def test_login_missing_fields(self, email, password, description):
        # Проверка ошибки при логине без обязательных полей.
        response = self.api.login_user(email=email, password=password)
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_UNAUTHORIZED, f"Ожидался код {HTTP_STATUS_UNAUTHORIZED}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is False, f"Поле {FIELD_SUCCESS} должно быть False"
        assert FIELD_MESSAGE in response_data, f"В ответе должно быть поле {FIELD_MESSAGE}"
        assert response_data[FIELD_MESSAGE] == ERROR_INCORRECT_CREDENTIALS, "Сообщение об ошибке не соответствует ожидаемому"