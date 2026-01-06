import requests
import allure


@allure.feature("Создание заказа")
@allure.story("POST /api/orders")
class TestCreateOrder:
    """Тесты для создания заказа"""
    
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, base_url, auth_headers, get_ingredients):
        """Тест создания заказа авторизованным пользователем с ингредиентами"""
        orders_url = f"{base_url}/orders"
        
        # Берем первые два ингредиента
        ingredient_ids = [ingredient["_id"] for ingredient in get_ingredients[:2]]
        order_data = {
            "ingredients": ingredient_ids
        }
        
        with allure.step("Отправить запрос на создание заказа"):
            response = requests.post(orders_url, json=order_data, headers=auth_headers)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        
        with allure.step("Проверить тело ответа"):
            data = response.json()
            assert data["success"] is True, "Поле success должно быть True"
            assert "name" in data, "В ответе должно быть поле name"
            assert "order" in data, "В ответе должно быть поле order"
            assert "number" in data["order"], "В ответе должно быть поле number в order"
            assert isinstance(data["order"]["number"], int), "Номер заказа должен быть числом"
    
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, base_url, get_ingredients):
        """Тест создания заказа неавторизованным пользователем
        
        По заданию без авторизации система должна вернуть ошибку (401).
        Тест проверяет правильное поведение согласно заданию.
        """
        orders_url = f"{base_url}/orders"
        
        # Берем первые два ингредиента
        ingredient_ids = [ingredient["_id"] for ingredient in get_ingredients[:2]]
        order_data = {
            "ingredients": ingredient_ids
        }
        
        with allure.step("Отправить запрос без авторизации"):
            response = requests.post(orders_url, json=order_data)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        
        with allure.step("Проверить тело ответа"):
            data = response.json()
            assert data["success"] is False, "Поле success должно быть False"
            assert "message" in data, "В ответе должно быть поле message"
    
    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients(self, base_url, auth_headers):
        """Тест создания заказа без ингредиентов"""
        orders_url = f"{base_url}/orders"
        order_data = {
            "ingredients": []
        }
        
        with allure.step("Отправить запрос без ингредиентов"):
            response = requests.post(orders_url, json=order_data, headers=auth_headers)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"
        
        with allure.step("Проверить тело ответа"):
            data = response.json()
            assert data["success"] is False, "Поле success должно быть False"
            assert "message" in data, "В ответе должно быть поле message"
            assert "must be provided" in data["message"].lower() or "required" in data["message"].lower(), \
                "Сообщение должно содержать информацию о необходимости ингредиентов"
    
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredient_hash(self, base_url, auth_headers):
        """Тест создания заказа с неверным хешем ингредиентов"""
        orders_url = f"{base_url}/orders"
        order_data = {
            "ingredients": ["invalid_hash_12345", "another_invalid_hash_67890"]
        }
        
        with allure.step("Отправить запрос с неверным хешем ингредиентов"):
            response = requests.post(orders_url, json=order_data, headers=auth_headers)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 500, f"Ожидался код 500, получен {response.status_code}"
        
        with allure.step("Проверить тело ответа"):
            # При ошибке 500 API может вернуть не JSON, проверяем наличие ответа
            assert response.text is not None, "Ответ должен содержать тело"
            # Если ответ в формате JSON, проверяем структуру
            try:
                data = response.json()
                assert "success" in data or "message" in data, \
                    "В ответе должно быть поле success или message"
            except ValueError:
                # Если ответ не JSON (например, HTML страница ошибки), это допустимо для 500
                pass
