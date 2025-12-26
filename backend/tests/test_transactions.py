import pytest
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


@pytest.fixture
def auth_header():
    ts = int(time.time())
    username = f"testuser_{ts}"
    password = "Password123!"

    client.post("/auth/register", json={"username": username, "password": password})
    response = client.post(
        "/auth/token", data={"username": username, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_user_registration_and_login():
    ts = int(time.time())
    unique_user = f"new_user_{ts}"
    reg_response = client.post(
        "/auth/register", json={"username": unique_user, "password": "SecurePassword1!"}
    )
    assert reg_response.status_code == 200
    assert "access_token" in reg_response.json()

    login_response = client.post(
        "/auth/token", data={"username": unique_user, "password": "SecurePassword1!"}
    )
    assert login_response.status_code == 200
    assert login_response.json()["token_type"] == "bearer"


# ... (Keep the rest of the tests as they were, they use the auth_header fixture)


def test_create_transaction(auth_header):
    response = client.post(
        "/transactions",
        json={
            "amount": 42.50,
            "category": "Food",
            "description": "Executive Lunch",
            "date": "2025-12-25",
        },
        headers=auth_header,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 42.50
    assert data["category"] == "Food"


def test_get_transactions(auth_header):
    response = client.get("/transactions", headers=auth_header)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_detailed_stats(auth_header):
    client.post(
        "/transactions",
        json={
            "amount": 100,
            "category": "Bills",
            "description": "Rent",
            "date": "2025-12-25",
        },
        headers=auth_header,
    )

    response = client.get("/transactions/stats/detailed", headers=auth_header)
    assert response.status_code == 200
    data = response.json()
    assert "monthly_burn" in data
    assert "categories" in data


def test_unauthorized_access():
    response = client.get("/transactions")
    assert response.status_code == 401


def test_generate_report_request(auth_header):
    response = client.post("/transactions/report", headers=auth_header)
    assert response.status_code == 200
