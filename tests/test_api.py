import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_articles_list():
    """Test article listing"""
    response = client.get("/articles")
    assert response.status_code == 200
    assert "articles" in response.json()
    assert "total" in response.json()

def test_stats():
    """Test stats"""
    response = client.get("/stats")
    assert response.status_code == 200
    assert "total_articles" in response.json()

def test_search():
    """Test semantic search"""
    response = client.post(
        "/search",
        json={"query": "artificial intelligence", "top_k": 5}
    )
    assert response.status_code == 200
    # Results should be a list
    assert isinstance(response.json(), list)