# Утилиты для работы с API.

import time
import random
import requests
from config.api_config import BASE_URL, ENDPOINTS


class APIHelper:
    # Класс для работы с API Stellar Burgers.
    
    def __init__(self):
        self.base_url = BASE_URL
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None
    
    def register_user(self, email=None, password=None, name=None):
        # Регистрация пользователя.
        url = self.base_url + ENDPOINTS["register"]
        data = {}
        if email is not None:
            data["email"] = email
        if password is not None:
            data["password"] = password
        if name is not None:
            data["name"] = name
        response = self.session.post(url, json=data)
        return response
    
    def login_user(self, email, password):
        # Авторизация пользователя.
        url = self.base_url + ENDPOINTS["login"]
        data = {
            "email": email,
            "password": password
        }
        response = self.session.post(url, json=data)
        
        # Сохраняем токены если авторизация успешна
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("success"):
                self.access_token = response_data.get("accessToken")
                self.refresh_token = response_data.get("refreshToken")
                # Устанавливаем токен в заголовки
                self.session.headers.update({
                    "Authorization": self.access_token
                })
        
        return response
    
    def logout_user(self):
        # Выход из системы.
        url = self.base_url + ENDPOINTS["logout"]
        data = {
            "token": self.refresh_token
        }
        response = self.session.post(url, json=data)
        return response
    
    def get_user_data(self):
        # Получение данных пользователя.
        url = self.base_url + ENDPOINTS["user"]
        response = self.session.get(url)
        return response
    
    def update_user_data(self, email=None, name=None, password=None):
        # Обновление данных пользователя.
        url = self.base_url + ENDPOINTS["user"]
        data = {}
        if email is not None:
            data["email"] = email
        if name is not None:
            data["name"] = name
        if password is not None:
            data["password"] = password
        
        response = self.session.patch(url, json=data)
        return response
    
    def create_order(self, ingredients):
        # Создание заказа.
        url = self.base_url + ENDPOINTS["orders"]
        data = {
            "ingredients": ingredients
        }
        response = self.session.post(url, json=data)
        return response
    
    def get_user_orders(self):
        # Получение заказов пользователя.
        url = self.base_url + ENDPOINTS["orders"]
        response = self.session.get(url)
        return response
    
    def get_ingredients(self):
        # Получение списка ингредиентов.
        url = self.base_url + ENDPOINTS["ingredients"]
        response = self.session.get(url)
        return response
    
    def clear_auth(self):
        # Очистка авторизации.
        self.access_token = None
        self.refresh_token = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]


def create_email():
    # Создание уникального email для тестов.
    timestamp = int(time.time())
    random_num = random.randint(1000, 9999)
    return f"test_user_{timestamp}_{random_num}@example.com"
