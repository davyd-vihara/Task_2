import pytest
import requests
import uuid
from constants import BASE_URL


@pytest.fixture
def base_url():
    """Базовый URL API"""
    return BASE_URL


@pytest.fixture
def create_user_data():
    """Создает уникальные данные пользователя для тестов"""
    unique_id = str(uuid.uuid4())[:8]
    return {
        "email": f"test_{unique_id}@example.com",
        "password": "password123",
        "name": f"TestUser_{unique_id}"
    }


@pytest.fixture
def registered_user(base_url, create_user_data):
    """Создает зарегистрированного пользователя и возвращает его данные"""
    register_url = f"{base_url}/auth/register"
    response = requests.post(register_url, json=create_user_data)
    
    data = response.json()
    
    access_token = data.get("accessToken", "")
    refresh_token = data.get("refreshToken", "")
    
    user_data = {
        "email": create_user_data["email"],
        "password": create_user_data["password"],
        "name": create_user_data["name"],
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    
    yield user_data
    
    # Удаление пользователя после теста
    try:
        delete_url = f"{base_url}/auth/user"
        headers = {"Authorization": access_token}
        requests.delete(delete_url, headers=headers)
    except Exception:
        pass  # Игнорируем ошибки при удалении


@pytest.fixture
def auth_headers(registered_user):
    """Возвращает заголовки авторизации для авторизованного пользователя"""
    return {"Authorization": registered_user["access_token"]}


@pytest.fixture
def get_ingredients(base_url):
    """Получает список ингредиентов для тестов"""
    ingredients_url = f"{base_url}/ingredients"
    response = requests.get(ingredients_url)
    data = response.json()
    # API может вернуть массив напрямую или объект с полем data
    ingredients = data if isinstance(data, list) else data.get("data", [])
    return ingredients
