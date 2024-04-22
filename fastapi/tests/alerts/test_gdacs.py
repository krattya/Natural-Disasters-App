from app.main import app
from fastapi.testclient import TestClient
import pytest

pytest.gdacs_id = ""


def test_get_all():
    with TestClient(app) as client:
        response = client.get("/api/v1/alerts/gdacs")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        if len(response.json()) > 0:
            pytest.gdacs_id = response.json()[0]["id"]


def test_get_one():
    if pytest.gdacs_id == "":
        pytest.skip("No gdacs alerts found")
    with TestClient(app) as client:
        response = client.get(f"/api/v1/alerts/gdacs/{pytest.gdacs_id}/")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
