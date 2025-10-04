from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "is_active": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
    assert data["is_active"] is True

def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) > 0
    assert users[0]["name"] == "Alice"

def test_update_user():
    response = client.put("/users/1", json={
        "id": 1,
        "name": "Alice Updated",
        "email": "alice_new@example.com",
        "is_active": True
    })
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["name"] == "Alice Updated"
    assert updated_user["email"] == "alice_new@example.com"

def test_deactivate_user():
    response = client.put("/users/1/deactivate")
    assert response.status_code == 200
    deactivated_user = response.json()
    assert deactivated_user["is_active"] is False
