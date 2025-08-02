import pytest
from .conftest import setup_database, teardown_database, client


@pytest.fixture(autouse=True)
def setup_and_teardown():
    setup_database()
    yield
    teardown_database()

@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "email": "test@test.pl",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",
    }

def test_read_users(test_user):
    client.post("/auth/register/",
        json=test_user)

    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Users retrieved successfully"
    assert isinstance(data["data"], list)

def test_read_users_empty():
    response = client.get("/users/")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Users not found"

def test_read_user(test_user):
    client.post("/auth/register/",
        json=test_user)
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "User retrieved successfully"
    assert data["data"]["username"] == test_user["username"]

def test_read_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"

def test_delete_user(test_user):
    register_response = client.post("/auth/register/", json=test_user)
    assert register_response.status_code == 201

    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.delete("/users/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "User deleted successfully"
    assert data["data"]["username"] == test_user["username"]

def test_delete_user_not_found():
    login_data = {
        "username": "nonexistentuser",
        "password": "password"
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 401

    response = client.delete("/users/999", headers={"Authorization": f"Bearer {login_response.json().get('access_token', '')}"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"

def test_update_user(test_user):
    client.post("/auth/register/", json=test_user)

    update_data = {
        "username": "updateduser",
        "email": "updateemail",
        "first_name": "Updated",
        "last_name": "UpdatedUser",
        "password": "updatedpassword"}
    response = client.put("/users/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "User updated successfully"
    assert data["data"]["username"] == update_data["username"]

def test_update_user_avatar(test_user):
    client.post("/auth/register/", json=test_user)

    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    test_file = {
        'file': ('test_avatar.png', b'test content', 'image/png')
    }

    response = client.put("/users/1/avatar",
                          files=test_file,
                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Avatar updated successfully"
    assert data["data"]["avatar_url"] is not None

def test_change_password(test_user):
    client.post("/auth/register/", json=test_user)

    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    change_password_data = {
        "old_password": test_user["password"],
        "new_password": "newpassword"
    }
    response = client.put("/users/1/change_password", data=change_password_data
                          , headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Password changed successfully"

def test_change_password_wrong_old_password(test_user):
    client.post("/auth/register/", json=test_user)

    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    change_password_data = {
        "old_password": "wrongpassword",
        "new_password": "newpassword"
    }
    response = client.put("/users/1/change_password", data=change_password_data
                          , headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Old password is incorrect"
