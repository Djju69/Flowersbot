"""
Базовые тесты для проверки функциональности
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
import sys
import os

# Добавляем путь к backend
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from backend.main import app

client = TestClient(app)

def test_health():
    """Тест health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_root():
    """Тест корневого endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data

def test_get_products():
    """Тест получения списка товаров"""
    response = client.get("/api/products")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    
    # Если есть товары, проверяем структуру
    if len(products) > 0:
        product = products[0]
        assert "id" in product
        assert "name" in product
        assert "price" in product
        assert "category" in product
        assert "photo_url" in product

def test_get_products_with_filters():
    """Тест получения товаров с фильтрами"""
    # Тест фильтра по категории
    response = client.get("/api/products?category=roses")
    assert response.status_code == 200
    
    # Тест фильтра по популярности
    response = client.get("/api/products?popular=true")
    assert response.status_code == 200

def test_get_product_by_id():
    """Тест получения товара по ID"""
    # Сначала получаем список товаров
    response = client.get("/api/products")
    assert response.status_code == 200
    products = response.json()
    
    if len(products) > 0:
        product_id = products[0]["id"]
        
        # Получаем товар по ID
        response = client.get(f"/api/products/{product_id}")
        assert response.status_code == 200
        
        product = response.json()
        assert product["id"] == product_id
        assert "name" in product
        assert "price" in product

def test_get_nonexistent_product():
    """Тест получения несуществующего товара"""
    response = client.get("/api/products/99999")
    assert response.status_code == 404

def test_create_order():
    """Тест создания заказа"""
    order_data = {
        "telegram_id": 123456,
        "name": "Test User",
        "phone": "+84901234567",
        "address": "Test Address, Nha Trang",
        "delivery_date": "2025-01-20",
        "delivery_time": "15:00-18:00",
        "items": [
            {
                "product_id": 1,
                "product_name": "Test Product",
                "size": "standard",
                "price": 500000,
                "quantity": 1
            }
        ],
        "items_total": 500000,
        "delivery_cost": 100000,
        "total": 600000
    }
    
    response = client.post("/api/orders", json=order_data)
    assert response.status_code == 200
    
    result = response.json()
    assert "order_id" in result
    assert "message" in result

def test_get_user_orders():
    """Тест получения заказов пользователя"""
    telegram_id = 123456
    response = client.get(f"/api/orders/{telegram_id}")
    assert response.status_code == 200
    
    orders = response.json()
    assert isinstance(orders, list)

def test_update_order_status():
    """Тест обновления статуса заказа"""
    # Сначала создаем заказ
    order_data = {
        "telegram_id": 123456,
        "name": "Test User",
        "phone": "+84901234567",
        "address": "Test Address",
        "delivery_date": "2025-01-20",
        "delivery_time": "15:00-18:00",
        "items": [],
        "items_total": 500000,
        "delivery_cost": 100000,
        "total": 600000
    }
    
    response = client.post("/api/orders", json=order_data)
    assert response.status_code == 200
    order_id = response.json()["order_id"]
    
    # Обновляем статус
    response = client.patch(f"/api/orders/{order_id}/status", params={"status": "confirmed"})
    assert response.status_code == 200

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
