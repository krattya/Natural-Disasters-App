from app.main import app
from fastapi.testclient import TestClient
import pytest

pytest.usgov_id = ""


def test_get_all():
    with TestClient(app) as client:
        response = client.get("/api/v1/alerts/gdacs")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        pytest.usgov_id = response.json()[0]["id"]


def test_get_one():
    with TestClient(app) as client:
        response = client.get(f"/api/v1/alerts/gdacs/{pytest.usgov_id}/")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
