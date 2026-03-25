import os

from fastapi.testclient import TestClient

os.environ.setdefault("MONGODB_URL", "mongodb://localhost:27017")
os.environ.setdefault("DB_NAME", "europe_travel_api_test")

from app.main import app


client = TestClient(app)


def test_root_endpoint_returns_service_message() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Europe Travel API is running."}


def test_health_endpoint_returns_ok_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
