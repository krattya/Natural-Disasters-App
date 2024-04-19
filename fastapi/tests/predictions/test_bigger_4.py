from app.main import app
from fastapi.testclient import TestClient


def test_get_all_earthquake_count():
    with TestClient(app) as client:
        response = client.get("/api/v1/predictions/earthquake-probabilities-bigger-4/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)
