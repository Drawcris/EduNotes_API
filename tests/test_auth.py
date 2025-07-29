import pytest
from .conftest import setup_database, teardown_database, client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    setup_database()
    yield
    teardown_database()

@pytest.fixture
def test_auth_data():
    return {
        "username": "testuser",
        "email": "test@wp.pl",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",}

def test_register(test_auth_data):
    response = client.post("/auth/register/", json=test_auth_data)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "User registered successfully"
    assert data["data"]["username"] == test_auth_data["username"]

def test_register_existing_user(test_auth_data):
    client.post("/auth/register/", json=test_auth_data)
    response = client.post("/auth/register/", json=test_auth_data)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Username or email already exists"

def test_login(test_auth_data):
    client.post("/auth/register/", json=test_auth_data)
    login_data = {
        "username": test_auth_data["username"],
        "password": test_auth_data["password"]
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(test_auth_data):
    login_data = {
        "username": test_auth_data["username"],
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Could not validate credentials"

