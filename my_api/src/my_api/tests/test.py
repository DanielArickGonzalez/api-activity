import pytest
from my_api.app import create_app
from uuid import uuid4

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_hello(client): 
    response = client.get('/') 
    assert response.status_code == 200 
    assert response.json == {"message": "Hello World!"}

def test_profile_requires_auth(client):
    response = client.get('/profile')
    assert response.status_code == 401
def test_profile_with_valid_auth(client):
    client.put(
        '/register',
        json={"username": "testuser", "password": "testpass123"}
    )
    response = client.get(
        '/profile',
        auth=("testuser", "testpass123")
    )
    assert response.status_code == 200
    assert "testuser" in response.json["message"]


def test_dashboard_requires_auth(client):
    response = client.get("/dashboard")
    assert response.status_code == 401


def test_dashboard_rejects_invalid_credentials(client):
    response = client.get("/dashboard", auth=("unknown-user", "wrong-password"))
    assert response.status_code == 401


def test_dashboard_with_valid_auth(client):
    username = f"dashboard_{uuid4().hex}"
    registration = client.put(
        "/register",
        json={"username": username, "password": "testpass123"},
    )
    assert registration.status_code == 201

    response = client.get(
        "/dashboard",
        auth=(username, "testpass123"),
    )
    assert response.status_code == 200
    assert response.json == {
        "message": f"Welcome to your dashboard, {username}!"
    }