from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_movie():
    response = client.post("/movies", json={
        "title": "Interstellar",
        "director": "Christopher Nolan",
        "year": 2014,
        "rating": 8.6
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Interstellar"


def test_get_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_movie():
    create = client.post("/movies", json={
        "title": "Old Title",
        "director": "Someone",
        "year": 2000,
        "rating": 5.0
    })
    movie_id = create.json()["id"]
    response = client.put(f"/movies/{movie_id}", json={
        "title": "New Title",
        "director": "Someone",
        "year": 2000,
        "rating": 7.0
    })
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"

def test_delete_movie():
    create = client.post("/movies", json={
        "title": "Delete Me",
        "director": "Test",
        "year": 2024,
        "rating": 6.0
    })
    movie_id = create.json()["id"]
    delete = client.delete(f"/movies/{movie_id}")
    assert delete.status_code == 200
    assert delete.json()["ok"] is True

