import requests
import allure
from constants import ENDPOINT_AUTH_LOGIN


@allure.feature("Логин пользователя")
@allure.story("POST /api/auth/login")
class TestLoginUser:
    """Тесты для логина пользователя"""
    
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, base_url, registered_user):
        """Тест логина под существующим пользователем"""
        login_url = f"{base_url}{ENDPOINT_AUTH_LOGIN}"
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        
        with allure.step("Отправить запрос на логин"):
            response = requests.post(login_url, json=login_data)
        
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        data = response.json()
        assert data["success"] is True, "Поле success должно быть True"
        assert "user" in data, "В ответе должно быть поле user"
        assert data["user"]["email"] == registered_user["email"], "Email не совпадает"
        assert data["user"]["name"] == registered_user["name"], "Имя не совпадает"
        assert "accessToken" in data, "В ответе должен быть accessToken"
        assert "refreshToken" in data, "В ответе должен быть refreshToken"
    
    @allure.title("Логин с неверным email")
    def test_login_with_wrong_email(self, base_url, registered_user):
        """Тест логина с неверным email"""
        login_url = f"{base_url}{ENDPOINT_AUTH_LOGIN}"
        login_data = {
            "email": "wrong_email@example.com",
            "password": registered_user["password"]
        }
        
        with allure.step("Отправить запрос с неверным email"):
            response = requests.post(login_url, json=login_data)
        
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        data = response.json()
        assert data["success"] is False, "Поле success должно быть False"
        assert "message" in data, "В ответе должно быть поле message"
        assert "incorrect" in data["message"].lower(), "Сообщение должно содержать информацию о неверных данных"
    
    @allure.title("Логин с неверным паролем")
    def test_login_with_wrong_password(self, base_url, registered_user):
        """Тест логина с неверным паролем"""
        login_url = f"{base_url}{ENDPOINT_AUTH_LOGIN}"
        login_data = {
            "email": registered_user["email"],
            "password": "wrong_password"
        }
        
        with allure.step("Отправить запрос с неверным паролем"):
            response = requests.post(login_url, json=login_data)
        
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        data = response.json()
        assert data["success"] is False, "Поле success должно быть False"
        assert "message" in data, "В ответе должно быть поле message"
        assert "incorrect" in data["message"].lower(), "Сообщение должно содержать информацию о неверных данных"
