import pytest
from .conftest import setup_database, teardown_database, client


@pytest.fixture(autouse=True)
def setup():
    setup_database()
    yield
    teardown_database()


@pytest.fixture
def test_organization():
    return {
        "organization_name": "Test Organization"
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
def test_channel(test_organization):
    return {
        "channel_name": "Test Channel",
        "organization_id": 1
    }


@pytest.fixture
def test_topic(test_channel):
    return {
        "topic_name": "Test Topic",
        "channel_id": 1,
        "organization_id": 1
    }

@pytest.fixture
def headers():
    return {"Authorization": "Bearer test-token"}

def test_get_my_notifications(headers, test_user, test_organization):
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

    response = client.post("/organizations/", json=test_organization, headers=auth_headers)
    assert response.status_code == 200

    # Usunięcie użytkownika z organizacji (generuje powiadomienie)
    response = client.delete(f"/organization_users/RemoveUserFromOrganization?organization_id=1&user_id=1", headers=auth_headers)
    assert response.status_code == 200

    response = client.get("/notifications/my", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Notifications retrieved successfully"
    assert isinstance(data["data"], list)

def test_get_my_notifications_no_auth():
    response = client.get("/notifications/my")
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Not authenticated"

def test_get_my_notifications_no_notifications(headers, test_user, test_organization):
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

    response = client.post("/organizations/", json=test_organization, headers=auth_headers)
    assert response.status_code == 200

    response = client.get("/notifications/my", headers=auth_headers)
    assert response.status_code == 404  # Zmieniono z 200 na 404
    data = response.json()
    assert data["detail"] == "No notifications found for this user"  # Zmieniono oczekiwaną wiadomość

def test_get_my_notifications_no_organization(headers, test_user):
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

    response = client.get("/notifications/my", headers=auth_headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No notifications found for this user"

def test_get_my_notifications_no_user(headers):
    response = client.get("/notifications/my", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No notifications found for this user"

def test_mark_notification_as_read(headers, test_user, test_organization):
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

    response = client.post("/organizations/", json=test_organization, headers=auth_headers)
    assert response.status_code == 200
    response = client.delete("/organization_users/RemoveUserFromOrganization?organization_id=1&user_id=1", headers=auth_headers)
    assert response.status_code == 200

    response = client.put("/notifications/1/read", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Notification marked as read successfully"
    assert data["data"]["status"] == "read"

def test_mark_nonexistent_notification_as_read(headers):
    response = client.put("/notifications/999/read", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Notification not found"

def test_delete_notification(headers, test_user, test_organization):
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

    response = client.post("/organizations/", json=test_organization, headers=auth_headers)
    assert response.status_code == 200
    response = client.delete("/organization_users/RemoveUserFromOrganization?organization_id=1&user_id=1", headers=auth_headers)
    assert response.status_code == 200

    response = client.delete("/notifications/1", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Notification deleted successfully"

def test_delete_nonexistent_notification(headers):
    response = client.delete("/notifications/999", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Notification not found"

def test_delete_all_notifications(headers, test_user, test_organization):
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

    response = client.post("/organizations/", json=test_organization, headers=auth_headers)
    assert response.status_code == 200
    response = client.delete("/organization_users/RemoveUserFromOrganization?organization_id=1&user_id=1", headers=auth_headers)
    assert response.status_code == 200

    # Usunięcie wszystkich powiadomień
    response = client.delete("/notifications/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "All notifications deleted successfully"
    assert isinstance(data["data"], list)

def test_delete_all_notifications_no_notifications(headers):
    response = client.delete("/notifications/", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No notifications found for this user"

def test_get_notification(headers, test_user, test_organization):
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

    response = client.post("/organizations/", json=test_organization, headers=auth_headers)
    assert response.status_code == 200
    response = client.delete("/organization_users/RemoveUserFromOrganization?organization_id=1&user_id=1", headers=auth_headers)
    assert response.status_code == 200

    response = client.get("/notifications/1", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Notification retrieved successfully"
    assert isinstance(data["data"], dict)

def test_get_nonexistent_notification(headers):
    response = client.get("/notifications/999", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Notification not found"