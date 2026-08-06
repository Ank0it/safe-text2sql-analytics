from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200


def test_invalid_request():

    response = client.post(
        "/query",
        json={}
    )

    assert response.status_code == 422