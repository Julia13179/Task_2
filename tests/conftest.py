# Фикстуры для тестов API.

import pytest
from config.api_helper import APIHelper, create_email
from config.api_config import TEST_USER_DATA
from tests.constants import USER_FIELD_PASSWORD, USER_FIELD_NAME


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

