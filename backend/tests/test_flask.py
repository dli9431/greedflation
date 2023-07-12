import pytest
from flask import json
from ..app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'message': 'Welcome to my web app!'}

def test_get_all(client):
    response = client.get('/api/get_all')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) > 0
    assert all('product_code' in item for item in data)
    assert all('name' in item for item in data)
    assert all('brand' in item for item in data)
    assert all('url' in item for item in data)