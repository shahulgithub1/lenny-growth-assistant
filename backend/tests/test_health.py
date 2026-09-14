"""
Tests for health check endpoint.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test health check endpoint returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["service"] == "lenny-growth-assistant"
    assert data["version"] == "1.0.0"


def test_health_check_fields():
    """Test health check response contains required fields."""
    response = client.get("/health")
    data = response.json()
    
    required_fields = ["status", "timestamp", "service", "version"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"
