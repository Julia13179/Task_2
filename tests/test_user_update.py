# Тесты для изменения данных пользователя.

import pytest
import allure
from config.api_helper import create_email
from config.api_config import TEST_USER_DATA
from tests.constants import (
    HTTP_STATUS_OK, HTTP_STATUS_UNAUTHORIZED, HTTP_STATUS_FORBIDDEN,
    FIELD_SUCCESS, FIELD_USER, FIELD_MESSAGE,
    USER_FIELD_EMAIL, USER_FIELD_PASSWORD, USER_FIELD_NAME,
    ERROR_UNAUTHORIZED, ERROR_EMAIL_EXISTS, FIELDS, FIELD_VALUES
)


@allure.feature("Изменение данных пользователя")
class TestUserUpdate:
    # Тесты для эндпоинта изменения данных пользователя.

    @allure.story("Успешное изменение данных")
    @allure.title("Изменение данных пользователя с авторизацией")
    @pytest.mark.parametrize("field,new_value", [
        (FIELDS[0], FIELD_VALUES[FIELDS[0]]),
        (FIELDS[1], FIELD_VALUES[FIELDS[1]]),
        (FIELDS[2], FIELD_VALUES[FIELDS[2]])
    ])
    def test_update_user_data_with_auth(self, registered_user_email, field, new_value):
        # Проверка изменения данных пользователя с авторизацией.
        # Логинимся
        self.api.login_user(
            email=registered_user_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD]
        )
        
        # Для email используем уникальный email
        if field == USER_FIELD_EMAIL:
            new_value = create_email()
        
        # Изменяем данные
        update_data = {field: new_value}
        response = self.api.update_user_data(**update_data)
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_OK, f"Ожидался код {HTTP_STATUS_OK}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is True, f"Поле {FIELD_SUCCESS} должно быть True"
        assert FIELD_USER in response_data, f"В ответе должно быть поле {FIELD_USER}"
        
        user_data = response_data[FIELD_USER]
        
        # Проверяем обновленные поля
        if field == USER_FIELD_EMAIL:
            assert user_data[USER_FIELD_EMAIL] == new_value, f"Поле {field} не обновилось"
        elif field == USER_FIELD_NAME:
            assert user_data[USER_FIELD_NAME] == new_value, f"Поле {field} не обновилось"
        elif field == USER_FIELD_PASSWORD:
            # Пароль не возвращается в ответе, проверяем только успешность операции
            pass
        
        # Проверяем, что другие поля остались неизменными
        if field != USER_FIELD_EMAIL:
            assert user_data[USER_FIELD_EMAIL] == registered_user_email, "Email не должен измениться"
        if field != USER_FIELD_NAME:
            assert user_data[USER_FIELD_NAME] == TEST_USER_DATA[USER_FIELD_NAME], "Имя не должно измениться"

    @allure.story("Ошибка без авторизации")
    @allure.title("Изменение данных пользователя без авторизации")
    @pytest.mark.parametrize("field,new_value", [
        (FIELDS[0], FIELD_VALUES[FIELDS[0]]),
        (FIELDS[1], FIELD_VALUES[FIELDS[1]]),
        (FIELDS[2], FIELD_VALUES[FIELDS[2]])
    ])
    def test_update_user_data_without_auth(self, registered_user_email, field, new_value):
        # Проверка ошибки при изменении данных без авторизации.
        # Не логинимся, пытаемся изменить данные
        update_data = {field: new_value}
        response = self.api.update_user_data(**update_data)
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_UNAUTHORIZED, f"Ожидался код {HTTP_STATUS_UNAUTHORIZED}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is False, f"Поле {FIELD_SUCCESS} должно быть False"
        assert FIELD_MESSAGE in response_data, f"В ответе должно быть поле {FIELD_MESSAGE}"
        assert response_data[FIELD_MESSAGE] == ERROR_UNAUTHORIZED, "Сообщение об ошибке не соответствует ожидаемому"

    @allure.story("Ошибка при дублировании email")
    @allure.title("Изменение email на уже существующий")
    def test_update_user_email_already_exists(self, registered_user_email):
        # Проверка ошибки при изменении email на уже существующий.
        # Создаем второго пользователя
        second_email = create_email()
        self.api.register_user(
            email=second_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD],
            name="Second User"
        )
        self.api.clear_auth()
        
        # Логинимся под первым пользователем
        self.api.login_user(
            email=registered_user_email,
            password=TEST_USER_DATA[USER_FIELD_PASSWORD]
        )
        
        # Пытаемся изменить email на email второго пользователя
        response = self.api.update_user_data(email=second_email)
        
        # Проверяем код ответа
        assert response.status_code == HTTP_STATUS_FORBIDDEN, f"Ожидался код {HTTP_STATUS_FORBIDDEN}, получен {response.status_code}"
        
        # Проверяем тело ответа
        response_data = response.json()
        assert response_data[FIELD_SUCCESS] is False, f"Поле {FIELD_SUCCESS} должно быть False"
        assert FIELD_MESSAGE in response_data, f"В ответе должно быть поле {FIELD_MESSAGE}"
        assert response_data[FIELD_MESSAGE] == ERROR_EMAIL_EXISTS, "Сообщение об ошибке не соответствует ожидаемому"