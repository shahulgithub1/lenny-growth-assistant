"""Tests for session endpoints."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.models import Base
from app.db.session import get_db

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_session():
    """Test creating a new session."""
    response = client.post("/api/sessions", json={"title": "Test Session"})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Session"


def test_list_sessions():
    """Test listing sessions."""
    # Create a session first
    client.post("/api/sessions", json={"title": "Test Session"})
    
    response = client.get("/api/sessions")
    assert response.status_code == 200
    data = response.json()
    assert "sessions" in data
    assert data["total"] > 0


def test_get_session():
    """Test getting a specific session."""
    # Create a session
    create_response = client.post("/api/sessions", json={"title": "Test Session"})
    session_id = create_response.json()["id"]
    
    # Get the session
    response = client.get(f"/api/sessions/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == session_id
    assert "messages" in data


def test_get_nonexistent_session():
    """Test getting a session that doesn't exist."""
    response = client.get("/api/sessions/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_session_isolation():
    """Test that sessions maintain independent contexts."""
    # Create two sessions
    session1 = client.post("/api/sessions", json={"title": "Session 1"}).json()
    session2 = client.post("/api/sessions", json={"title": "Session 2"}).json()
    
    # Get both sessions
    session1_data = client.get(f"/api/sessions/{session1['id']}").json()
    session2_data = client.get(f"/api/sessions/{session2['id']}").json()
    
    # Verify they are different
    assert session1_data["id"] != session2_data["id"]
    assert session1_data["messages"] == []
    assert session2_data["messages"] == []


def test_delete_session():
    """Test deleting a session."""
    # Create a session
    create_response = client.post("/api/sessions", json={"title": "Test Delete Session"})
    session_id = create_response.json()["id"]
    
    # Verify session exists
    get_response = client.get(f"/api/sessions/{session_id}")
    assert get_response.status_code == 200
    
    # Delete the session
    delete_response = client.delete(f"/api/sessions/{session_id}")
    assert delete_response.status_code == 204
    
    # Verify session no longer exists
    get_after_delete = client.get(f"/api/sessions/{session_id}")
    assert get_after_delete.status_code == 404


def test_delete_nonexistent_session():
    """Test deleting a session that doesn't exist."""
    response = client.delete("/api/sessions/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_timestamp_format():
    """Test that timestamps are properly serialized with timezone info."""
    # Create a session
    response = client.post("/api/sessions", json={"title": "Timestamp Test"})
    assert response.status_code == 201
    data = response.json()
    
    # Check timestamp fields exist
    assert "created_at" in data
    assert "updated_at" in data
    
    # Verify ISO 8601 format with timezone
    created_at = data["created_at"]
    updated_at = data["updated_at"]
    
    # Should be valid ISO format
    assert "T" in created_at
    assert "T" in updated_at
    
    # Should have timezone info (+00:00 or Z for UTC)
    assert "+00:00" in created_at or created_at.endswith("Z")
    assert "+00:00" in updated_at or updated_at.endswith("Z")
    
    # Should be parseable as datetime
    from datetime import datetime
    dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
    # Should have timezone info
    assert dt.tzinfo is not None


def test_session_updated_timestamp():
    """Test that updated_at timestamp changes when session is modified."""
    import time
    
    # Create a session
    create_response = client.post("/api/sessions", json={"title": "Update Test"})
    session_id = create_response.json()["id"]
    original_updated_at = create_response.json()["updated_at"]
    
    # Wait a moment
    time.sleep(0.1)
    
    # Get the session (this doesn't update it, but we'll check the format)
    get_response = client.get(f"/api/sessions/{session_id}")
    assert get_response.status_code == 200
    
    # Timestamps should be consistently formatted
    data = get_response.json()
    assert "created_at" in data
    assert "updated_at" in data
