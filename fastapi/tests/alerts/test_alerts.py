from app.main import app
from fastapi.testclient import TestClient


# PYTHONPATH=. pytest
# isntall pytest
# pip install httpx
# pip install -U pytest


def test_alerts():
    with TestClient(app) as client:
        response = client.get("/api/v1/alerts/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
