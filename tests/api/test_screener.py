from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_screener_min_roe():
    response = client.get("/api/v1/screener?min_roe=15")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for company in data:
        assert company["roe_percentage"] >= 15


def test_screener_invalid_parameter():
    response = client.get("/api/v1/screener?min_roe=abc")

    assert response.status_code == 422
