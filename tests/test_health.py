"""Unit tests for health endpoints."""
from fastapi.testclient import TestClient
import sys
import os

# Ensure project root in path for imports
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.append(ROOT)

from backend.app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("status") == "ok"


def test_ready() -> None:
    response = client.get("/api/ready")
    assert response.status_code == 200
    payload = response.json()
    assert payload.get("status") == "ready"
