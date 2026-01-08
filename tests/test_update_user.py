import requests
import allure
import uuid
from constants import ENDPOINT_AUTH_USER, ENDPOINT_AUTH_LOGIN


@allure.feature("Изменение данных пользователя")
@allure.story("PATCH /api/auth/user")
class TestUpdateUser:
    """Тесты для изменения данных пользователя"""
    
    @allure.title("Изменение email с авторизацией")
    def test_update_email_with_auth(self, base_url, registered_user, auth_headers):
        """Тест изменения email авторизованным пользователем"""
        update_url = f"{base_url}{ENDPOINT_AUTH_USER}"
        unique_id = str(uuid.uuid4())[:8]
        new_email = f"updated_{unique_id}@example.com"
        update_data = {
            "email": new_email
        }
        
        with allure.step("Отправить запрос на изменение email"):
            response = requests.patch(update_url, json=update_data, headers=auth_headers)
        
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        data = response.json()
        assert data["success"] is True, "Поле success должно быть True"
        assert "user" in data, "В ответе должно быть поле user"
        assert data["user"]["email"] == new_email, "Email должен быть обновлен"
    
    @allure.title("Изменение name с авторизацией")
    def test_update_name_with_auth(self, base_url, registered_user, auth_headers):
        """Тест изменения name авторизованным пользователем"""
        update_url = f"{base_url}{ENDPOINT_AUTH_USER}"
        unique_id = str(uuid.uuid4())[:8]
        new_name = f"UpdatedName_{unique_id}"
        update_data = {
            "name": new_name
        }
        
        with allure.step("Отправить запрос на изменение name"):
            response = requests.patch(update_url, json=update_data, headers=auth_headers)
        
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        data = response.json()
        assert data["success"] is True, "Поле success должно быть True"
        assert "user" in data, "В ответе должно быть поле user"
        assert data["user"]["name"] == new_name, "Имя должно быть обновлено"
    
    @allure.title("Изменение password с авторизацией")
    def test_update_password_with_auth(self, base_url, registered_user, auth_headers):
        """Тест изменения password авторизованным пользователем"""
        update_url = f"{base_url}{ENDPOINT_AUTH_USER}"
        new_password = "new_password123"
        update_data = {
            "password": new_password
        }
        
        with allure.step("Отправить запрос на изменение password"):
            response = requests.patch(update_url, json=update_data, headers=auth_headers)
        
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        data = response.json()
        assert data["success"] is True, "Поле success должно быть True"
        assert "user" in data, "В ответе должно быть поле user"
    
    @allure.title("Логин с обновленным паролем после изменения password")
    def test_login_with_updated_password(self, base_url, registered_user, auth_headers):
        """Тест логина с обновленным паролем для проверки, что пароль действительно изменился"""
        update_url = f"{base_url}{ENDPOINT_AUTH_USER}"
        new_password = "new_password123"
        update_data = {
            "password": new_password
        }
        
        with allure.step("Отправить запрос на изменение password"):
            requests.patch(update_url, json=update_data, headers=auth_headers)
        
        with allure.step("Отправить запрос на логин с новым паролем"):
            login_url = f"{base_url}{ENDPOINT_AUTH_LOGIN}"
            login_data = {
                "email": registered_user["email"],
                "password": new_password
            }
            login_response = requests.post(login_url, json=login_data)
        
        assert login_response.status_code == 200, "Логин с новым паролем должен быть успешным"
        login_data_response = login_response.json()
        assert login_data_response["success"] is True, "Логин должен быть успешным"
    
    @allure.title("Изменение всех полей с авторизацией")
    def test_update_all_fields_with_auth(self, base_url, registered_user, auth_headers):
        """Тест изменения всех полей авторизованным пользователем"""
        update_url = f"{base_url}{ENDPOINT_AUTH_USER}"
        unique_id = str(uuid.uuid4())[:8]
        update_data = {
            "email": f"all_fields_{unique_id}@example.com",
            "name": f"AllFields_{unique_id}",
            "password": "new_password456"
        }
        
        with allure.step("Отправить запрос на изменение всех полей"):
            response = requests.patch(update_url, json=update_data, headers=auth_headers)
        
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        data = response.json()
        assert data["success"] is True, "Поле success должно быть True"
        assert "user" in data, "В ответе должно быть поле user"
        assert data["user"]["email"] == update_data["email"], "Email должен быть обновлен"
        assert data["user"]["name"] == update_data["name"], "Имя должно быть обновлено"
    
    @allure.title("Изменение name без авторизации")
    def test_update_name_without_auth(self, base_url, create_user_data):
        """Тест изменения name неавторизованным пользователем"""
        update_url = f"{base_url}{ENDPOINT_AUTH_USER}"
        update_data = {
            "name": "UnauthorizedUser"
        }
        
        with allure.step("Отправить запрос без авторизации"):
            response = requests.patch(update_url, json=update_data)
        
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        data = response.json()
        assert data["success"] is False, "Поле success должно быть False"
        assert "message" in data, "В ответе должно быть поле message"
        assert "authorised" in data["message"].lower() or "authorized" in data["message"].lower(), \
            "Сообщение должно содержать информацию о необходимости авторизации"
    
    @allure.title("Изменение email без авторизации")
    def test_update_email_without_auth(self, base_url, create_user_data):
        """Тест изменения email неавторизованным пользователем"""
        update_url = f"{base_url}{ENDPOINT_AUTH_USER}"
        unique_id = str(uuid.uuid4())[:8]
        update_data = {
            "email": f"unauthorized_{unique_id}@example.com"
        }
        
        with allure.step("Отправить запрос без авторизации"):
            response = requests.patch(update_url, json=update_data)
        
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        data = response.json()
        assert data["success"] is False, "Поле success должно быть False"
        assert "message" in data, "В ответе должно быть поле message"
        assert "authorised" in data["message"].lower() or "authorized" in data["message"].lower(), \
            "Сообщение должно содержать информацию о необходимости авторизации"
    
    @allure.title("Изменение password без авторизации")
    def test_update_password_without_auth(self, base_url, create_user_data):
        """Тест изменения password неавторизованным пользователем"""
        update_url = f"{base_url}{ENDPOINT_AUTH_USER}"
        update_data = {
            "password": "unauthorized_password"
        }
        
        with allure.step("Отправить запрос без авторизации"):
            response = requests.patch(update_url, json=update_data)
        
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        data = response.json()
        assert data["success"] is False, "Поле success должно быть False"
        assert "message" in data, "В ответе должно быть поле message"
        assert "authorised" in data["message"].lower() or "authorized" in data["message"].lower(), \
            "Сообщение должно содержать информацию о необходимости авторизации"
