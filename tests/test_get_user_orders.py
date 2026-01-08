import requests
import allure
from constants import ENDPOINT_ORDERS


@allure.feature("Получение заказов пользователя")
@allure.story("GET /api/orders")
class TestGetUserOrders:
    """Тесты для получения заказов конкретного пользователя"""
    
    @allure.title("Получение заказов авторизованным пользователем")
    def test_get_orders_with_auth(self, base_url, auth_headers, get_ingredients):
        """Тест получения заказов авторизованным пользователем"""
        orders_url = f"{base_url}{ENDPOINT_ORDERS}"
        
        with allure.step("Создать заказ для теста"):
            create_order_url = f"{base_url}{ENDPOINT_ORDERS}"
            ingredient_ids = [ingredient["_id"] for ingredient in get_ingredients[:2]]
            order_data = {
                "ingredients": ingredient_ids
            }
            requests.post(create_order_url, json=order_data, headers=auth_headers)
        
        with allure.step("Отправить запрос на получение заказов"):
            response = requests.get(orders_url, headers=auth_headers)
        
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        data = response.json()
        assert data["success"] is True, "Поле success должно быть True"
        assert "orders" in data, "В ответе должно быть поле orders"
        assert isinstance(data["orders"], list), "Поле orders должно быть списком"
        assert "total" in data, "В ответе должно быть поле total"
        assert "totalToday" in data, "В ответе должно быть поле totalToday"
        assert isinstance(data["total"], int), "Поле total должно быть числом"
        assert isinstance(data["totalToday"], int), "Поле totalToday должно быть числом"
    
    @allure.title("Проверка структуры заказа при получении заказов")
    def test_get_orders_structure(self, base_url, auth_headers, get_ingredients):
        """Тест проверки структуры заказа при получении заказов"""
        orders_url = f"{base_url}{ENDPOINT_ORDERS}"
        
        with allure.step("Создать заказ для теста"):
            create_order_url = f"{base_url}{ENDPOINT_ORDERS}"
            ingredient_ids = [ingredient["_id"] for ingredient in get_ingredients[:2]]
            order_data = {
                "ingredients": ingredient_ids
            }
            requests.post(create_order_url, json=order_data, headers=auth_headers)
        
        with allure.step("Отправить запрос на получение заказов"):
            response = requests.get(orders_url, headers=auth_headers)
        
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        data = response.json()
        assert len(data["orders"]) > 0, "Должен быть хотя бы один заказ"
        order = data["orders"][0]
        assert "_id" in order, "В заказе должно быть поле _id"
        assert "ingredients" in order, "В заказе должно быть поле ingredients"
        assert "status" in order, "В заказе должно быть поле status"
        assert "number" in order, "В заказе должно быть поле number"
        assert "createdAt" in order, "В заказе должно быть поле createdAt"
        assert "updatedAt" in order, "В заказе должно быть поле updatedAt"
    
    @allure.title("Получение заказов неавторизованным пользователем")
    def test_get_orders_without_auth(self, base_url):
        """Тест получения заказов неавторизованным пользователем"""
        orders_url = f"{base_url}{ENDPOINT_ORDERS}"
        
        with allure.step("Отправить запрос без авторизации"):
            response = requests.get(orders_url)
        
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"
        data = response.json()
        assert data["success"] is False, "Поле success должно быть False"
        assert "message" in data, "В ответе должно быть поле message"
        assert ("authorised" in data["message"].lower() or
                "authorized" in data["message"].lower()), \
            "Сообщение должно содержать информацию о необходимости авторизации"
