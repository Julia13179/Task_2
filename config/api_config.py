# Конфигурация для тестов API Stellar Burgers.

# Базовый URL API
BASE_URL = "https://stellarburgers.education-services.ru/api"

# Эндпоинты API
ENDPOINTS = {
    "register": "/auth/register",
    "login": "/auth/login", 
    "logout": "/auth/logout",
    "user": "/auth/user",
    "token": "/auth/token",
    "password_reset": "/password-reset",
    "password_reset_reset": "/password-reset/reset",
    "ingredients": "/ingredients",
    "orders": "/orders",
    "orders_all": "/orders/all"
}

# Тестовые данные
TEST_USER_DATA = {
    "email": "test_user@example.com",
    "password": "test_password123",
    "name": "Test User"
}

# Невалидные ингредиенты
INVALID_INGREDIENTS = [
    "invalid_hash_1",
    "invalid_hash_2"
]
