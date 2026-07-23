from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_get_all_sectors():
    response = client.get("/api/v1/sectors")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 10
    assert "Information Technology" in data


def test_get_information_technology_sector():
    response = client.get("/api/v1/sectors/Information%20Technology")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for company in data:
        assert company["sector"] == "Information Technology"
