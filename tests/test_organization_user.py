import pytest
from .conftest import setup_database, teardown_database, client
from models.organization_user import UserRoleEnum

@pytest.fixture(autouse=True)
def setup_and_teardown():
    setup_database()
    yield
    teardown_database()

@pytest.fixture
def test_organization():
    return {
        "organization_name": "Test Organization",
    }

@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword",
        "first_name": "Test",
        "last_name": "User",
    }

@pytest.fixture
def test_user2():
    return {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpassword2",
        "first_name": "Test2",
        "last_name": "User2",
    }

def test_create_organization_user(test_organization, test_user, test_user2):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    login_response = client.post("/auth/login", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert response.status_code == 201
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200
    organization_id = response.json()["data"]["organization_id"]

    response = client.post("/auth/register", json=test_user2)
    assert response.status_code == 201
    user2_id = response.json()["data"]["user_id"]

    response = client.post(
        "/organization_users/",
        params={"organization_id": organization_id, "user_id": user2_id, "role": UserRoleEnum.user.value},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_get_organization_users(test_organization, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    login_response = client.post("/auth/login", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert response.status_code == 201
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200
    organization_id = response.json()["data"]["organization_id"]

    response = client.get(f"/organization_users/{organization_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert isinstance(response.json()["data"], list)

def test_remove_user_from_organization(test_organization, test_user, test_user2):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    login_response = client.post("/auth/login", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/organizations/", json=test_organization, headers=headers)
    organization_id = response.json()["data"]["organization_id"]

    response = client.post("/auth/register", json=test_user2)
    user2_id = response.json()["data"]["user_id"]

    response = client.post(
        "/organization_users/",
        params={"organization_id": organization_id, "user_id": user2_id, "role": UserRoleEnum.user.value},
        headers=headers
    )

    response = client.delete(
        "/organization_users/RemoveUserFromOrganization",
        params={"organization_id": organization_id, "user_id": user2_id},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_get_current_user_organizations(test_organization, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    login_response = client.post("/auth/login", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200

    response = client.get("/organization_users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert isinstance(response.json()["data"], list)