import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_create_course():
    response = client.post(
        "/courses/",
        json={"id": 1, "title": "Math 101", "description": "Basic Math"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Math 101"
    assert data["description"] == "Basic Math"

def test_read_course():
    # create the course first
    client.post(
        "/courses/",
        json={"id": 2, "title": "History 101", "description": "World History"}
    )

    # now read it back
    response = client.get("/courses/2")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 2
    assert data["title"] == "History 101"
    assert data["description"] == "World History"
