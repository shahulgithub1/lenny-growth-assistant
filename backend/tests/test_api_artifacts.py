"""Tests for artifact API endpoints."""
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4

from app.main import app
from app.db.models import Artifact
from app.db.session import get_db


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


def test_get_artifact_not_found(client):
    """Test 404 when artifact doesn't exist."""
    fake_id = str(uuid4())
    response = client.get(f"/api/artifacts/{fake_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_session_artifacts_empty(client):
    """Test listing artifacts for session with none."""
    session_id = str(uuid4())
    response = client.get(f"/api/sessions/{session_id}/artifacts")
    assert response.status_code == 200
    assert response.json() == []
