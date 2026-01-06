import requests
import allure


@allure.feature("Создание пользователя")
@allure.story("POST /api/auth/register")
class TestCreateUser:
    """Тесты для создания пользователя"""
    
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, base_url, create_user_data):
        """Тест создания уникального пользователя"""
        register_url = f"{base_url}/auth/register"
        
        with allure.step("Отправить запрос на создание пользователя"):
            response = requests.post(register_url, json=create_user_data)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        
        with allure.step("Проверить тело ответа"):
            data = response.json()
            assert data["success"] is True, "Поле success должно быть True"
            assert "user" in data, "В ответе должно быть поле user"
            assert data["user"]["email"] == create_user_data["email"], "Email не совпадает"
            assert data["user"]["name"] == create_user_data["name"], "Имя не совпадает"
            assert "accessToken" in data, "В ответе должен быть accessToken"
            assert "refreshToken" in data, "В ответе должен быть refreshToken"
    
    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, base_url, registered_user):
        """Тест создания пользователя, который уже зарегистрирован"""
        register_url = f"{base_url}/auth/register"
        user_data = {
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"]
        }
        
        with allure.step("Отправить запрос на создание существующего пользователя"):
            response = requests.post(register_url, json=user_data)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
        
        with allure.step("Проверить тело ответа"):
            data = response.json()
            assert data["success"] is False, "Поле success должно быть False"
            assert "message" in data, "В ответе должно быть поле message"
            assert "already exists" in data["message"].lower(), "Сообщение должно содержать информацию о существующем пользователе"
    
    @allure.title("Создание пользователя без обязательного поля email")
    def test_create_user_without_email(self, base_url, create_user_data):
        """Тест создания пользователя без поля email"""
        register_url = f"{base_url}/auth/register"
        user_data = {
            "password": create_user_data["password"],
            "name": create_user_data["name"]
        }
        
        with allure.step("Отправить запрос без поля email"):
            response = requests.post(register_url, json=user_data)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
        
        with allure.step("Проверить тело ответа"):
            data = response.json()
            assert data["success"] is False, "Поле success должно быть False"
            assert "message" in data, "В ответе должно быть поле message"
            assert "required" in data["message"].lower(), "Сообщение должно содержать информацию об обязательных полях"
    
    @allure.title("Создание пользователя без обязательного поля password")
    def test_create_user_without_password(self, base_url, create_user_data):
        """Тест создания пользователя без поля password"""
        register_url = f"{base_url}/auth/register"
        user_data = {
            "email": create_user_data["email"],
            "name": create_user_data["name"]
        }
        
        with allure.step("Отправить запрос без поля password"):
            response = requests.post(register_url, json=user_data)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
        
        with allure.step("Проверить тело ответа"):
            data = response.json()
            assert data["success"] is False, "Поле success должно быть False"
            assert "message" in data, "В ответе должно быть поле message"
            assert "required" in data["message"].lower(), "Сообщение должно содержать информацию об обязательных полях"
    
    @allure.title("Создание пользователя без обязательного поля name")
    def test_create_user_without_name(self, base_url, create_user_data):
        """Тест создания пользователя без поля name"""
        register_url = f"{base_url}/auth/register"
        user_data = {
            "email": create_user_data["email"],
            "password": create_user_data["password"]
        }
        
        with allure.step("Отправить запрос без поля name"):
            response = requests.post(register_url, json=user_data)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"
        
        with allure.step("Проверить тело ответа"):
            data = response.json()
            assert data["success"] is False, "Поле success должно быть False"
            assert "message" in data, "В ответе должно быть поле message"
            assert "required" in data["message"].lower(), "Сообщение должно содержать информацию об обязательных полях"
