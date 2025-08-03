import pytest
from .conftest import setup_database, teardown_database, client, headers, test_user


@pytest.fixture(autouse=True)
def setup():
    setup_database()
    yield
    teardown_database()

def test_get_my_score(headers, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    login_data = {
        "username": test_user["username"],
        "password": test_user["password"]
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json().get("access_token")
    auth_headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/ranking/my", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "User score retrieved successfully"
    assert "username" in data["data"]
    assert "score" in data["data"]
    assert "rank" in data["data"]

def test_get_all_users_score(headers, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    response = client.get("/ranking/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "All users scores retrieved successfully"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert "username" in data["data"][0]
    assert "score" in data["data"][0]
    assert "rank" in data["data"][0]

def test_get_user_score(headers, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    response = client.get("/ranking/1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "User score retrieved successfully"
    assert "username" in data["data"]
    assert "score" in data["data"]
    assert "rank" in data["data"]

def test_get_nonexistent_user_score(headers):
    response = client.get("/ranking/999", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"

def test_get_all_users_score_no_users(headers):
    response = client.get("/ranking/", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No users found"

def test_get_my_score_unauthorized():
    response = client.get("/ranking/my")
    assert response.status_code == 401