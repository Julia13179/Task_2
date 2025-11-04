# Константы для тестов API Stellar Burgers.

# HTTP статус коды
HTTP_STATUS_OK = 200
HTTP_STATUS_BAD_REQUEST = 400
HTTP_STATUS_UNAUTHORIZED = 401
HTTP_STATUS_FORBIDDEN = 403
HTTP_STATUS_INTERNAL_SERVER_ERROR = 500

# Поля ответа API
FIELD_SUCCESS = "success"
FIELD_USER = "user"
FIELD_ACCESS_TOKEN = "accessToken"
FIELD_REFRESH_TOKEN = "refreshToken"
FIELD_MESSAGE = "message"
FIELD_NAME = "name"
FIELD_ORDER = "order"
FIELD_NUMBER = "number"
FIELD_ORDERS = "orders"
FIELD_TOTAL = "total"
FIELD_TOTAL_TODAY = "totalToday"
FIELD_INGREDIENTS = "ingredients"
FIELD_DATA = "data"
FIELD_ID = "_id"
FIELD_STATUS = "status"
FIELD_CREATED_AT = "createdAt"
FIELD_UPDATED_AT = "updatedAt"

# Поля пользователя
USER_FIELD_EMAIL = "email"
USER_FIELD_PASSWORD = "password"
USER_FIELD_NAME = "name"

# Сообщения об ошибках
ERROR_USER_ALREADY_EXISTS = "User already exists"
ERROR_REQUIRED_FIELDS = "Email, password and name are required fields"
ERROR_INCORRECT_CREDENTIALS = "email or password are incorrect"
ERROR_UNAUTHORIZED = "You should be authorised"
ERROR_EMAIL_EXISTS = "User with such email already exists"
ERROR_INGREDIENTS_REQUIRED = "Ingredient ids must be provided"

# Тестовые значения
MIN_INGREDIENTS = 2
EMPTY_LIST = []
EMPTY_STRING = ""

# Тестовые данные для параметризации
TEST_EMAILS = [
    "nonexistent@example.com",
    "test_user@example.com",
    ""
]

TEST_PASSWORDS = [
    "test_password123",
    "wrong_password",
    ""
]

FIELDS = [USER_FIELD_EMAIL, USER_FIELD_PASSWORD, USER_FIELD_NAME]

FIELD_VALUES = {
    USER_FIELD_EMAIL: "unique_new_email@example.com",
    USER_FIELD_NAME: "New Name", 
    USER_FIELD_PASSWORD: "new_password123"
}

# Описания для параметризации
INVALID_DESC = [
    "неверный email",
    "неверный пароль", 
    "неверный email и пароль"
]

MISSING_DESC = [
    "пустой email",
    "пустой пароль",
    "пустые email и пароль"
]
