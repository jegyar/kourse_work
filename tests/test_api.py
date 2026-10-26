import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Auto Parts Store API is running"}

def test_get_categories():
    response = client.get("/products/categories")
    assert response.status_code == 200
    categories = response.json()
    assert isinstance(categories, list)
    assert len(categories) > 0

def test_get_brands():
    response = client.get("/products/brands")
    assert response.status_code == 200
    brands = response.json()
    assert isinstance(brands, list)
    assert len(brands) > 0

def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) > 0
