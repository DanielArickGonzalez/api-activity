import pytest
from api_activity.app import create_app

@pytest.fixture 
def client(): 
    with create_app().test_client() as client: 
        yield client

def test_hello(client): 
    response = client.get('/') 
    assert response.status_code == 200 
    assert response.json == {"message": "Hello World!"}
