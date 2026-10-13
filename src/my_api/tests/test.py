import pytest
from my-api.app import create_app

@pytest.fixture 
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