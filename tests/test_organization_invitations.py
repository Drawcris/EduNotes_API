import pytest
from .conftest import setup_database, teardown_database, client, test_organization
from fastapi.testclient import TestClient
from models.organization_user import UserRoleEnum
from models.organization_invitations import InvitedUserRoleEnum
from routers.organizations import router as organizations_router

@pytest.fixture(autouse=True)
def setup_and_teardown():
    setup_database()
    yield
    teardown_database()

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
def test_organization_user():
    return {
        "organization_id": 1,
        "user_id": 1,
        "role": UserRoleEnum.owner.value,
    }

@pytest.fixture
def test_user2():
    return {
        "username": "testuser2",
        "email": "test@example2.com",
        "password": "testpassword2",
        "first_name": "Test2",
        "last_name": "User2",
    }

def test_invite_user(test_organization, test_user, test_user2):
    # Register and login first user (owner)
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    login_response = client.post("/auth/login", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create organization
    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200
    organization_id = response.json()["data"]["organization_id"]

    # Register second user
    response = client.post("/auth/register", json=test_user2)
    assert response.status_code == 201

    # Send invitation
    response = client.post(
        f"/organization-invitations/",
        params={"organization_id": organization_id, "email": test_user2["email"], "role": InvitedUserRoleEnum.user.value},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Invitation sent successfully"
    assert data["data"]["email"] == test_user2["email"]

def test_invite_nonexistent_user(test_organization, test_user):
    # Register and login first user
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    login_response = client.post("/auth/login", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create organization
    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200
    organization_id = response.json()["data"]["organization_id"]

    # Try to invite nonexistent user
    response = client.post(
        f"/organization-invitations/",
        params={"organization_id": organization_id, "email": "nonexistent@email.com", "role": InvitedUserRoleEnum.user.value},
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User with this email does not exist"

def test_get_sent_invitations(test_organization, test_user, test_user2):
    # Register and login first user
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    login_response = client.post("/auth/login", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create organization
    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200
    organization_id = response.json()["data"]["organization_id"]

    # Register second user
    response = client.post("/auth/register", json=test_user2)
    assert response.status_code == 201

    # Send invitation
    response = client.post(
        f"/organization-invitations/",
        params={"organization_id": organization_id, "email": test_user2["email"], "role": InvitedUserRoleEnum.user.value},
        headers=headers
    )
    assert response.status_code == 200

    # Get sent invitations
    response = client.get("/organization-invitations/sent", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Sent invitations retrieved successfully"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0

def test_accept_nonexistent_invitation(test_user):
    # Register and login user
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    login_response = client.post("/auth/login", data={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Try to accept nonexistent invitation
    response = client.post(
        "/organization-invitations/999/accept",
        headers=headers
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Invitation not found"

def test_get_invitations_unauthorized():
    # Try to get invitations without authorization
    response = client.get("/organization-invitations/my")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

    response = client.get("/organization-invitations/sent")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"