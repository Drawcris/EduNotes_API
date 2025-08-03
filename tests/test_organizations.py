import pytest
from .conftest import setup_database, teardown_database, client, test_organization
from fastapi.testclient import TestClient
from routers.organizations import router as organizations_router

@pytest.fixture(autouse=True)
def setup_and_teardown():
    setup_database()
    yield
    teardown_database()

def test_create_organization(test_organization):
        response = client.post(
            "/organizations/",
            json=test_organization,
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Organization created successfully"
        assert data["data"]["organization_name"] == test_organization["organization_name"]

def test_create_organization_invalid_data():
        response = client.post(
            "/organizations/",
            json={},
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 422
        data = response.json()
        assert data["detail"][0]["msg"] == "Field required"
        assert data["detail"][0]["type"] == "missing"
        assert data["detail"][0]["loc"] == ["body", "organization_name"]

def test_create_organization_unauthorized():
        response = client.post(
            "/organizations/",
            json={"organization_name": "Unauthorized Organization"},
            headers={}
        )
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Not authenticated"

def test_create_existing_organization(test_organization):
        client.post(
            "/organizations/",
            json=test_organization,
            headers={"Authorization": "Bearer test-token"}
        )
        response = client.post(
            "/organizations/",
            json=test_organization,
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Organization with this name already exists"

def test_read_organizations(test_organization):
        client.post(
            "/organizations/",
            json=test_organization,
            headers={"Authorization": "Bearer test-token"}
        )
        response = client.get(
            "/organizations/"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Organizations retrieved successfully"
        assert isinstance(data["data"], list)

def test_read_organization(test_organization):
        client.post(
            "/organizations/",
            json=test_organization,
            headers={"Authorization": "Bearer test-token"}
        )
        response = client.get(
            "/organizations/1",
        )

        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Organization retrieved successfully"
        assert data["data"]["organization_name"] == test_organization["organization_name"]

def test_read_organization_not_found():
        response = client.get(
            "/organizations/999",
        )
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Organization not found"

def test_delete_organization(test_organization):
        client.post(
            "/organizations/",
            json=test_organization,
            headers={"Authorization": "Bearer test-token"}
        )
        response = client.delete(
            "/organizations/1",
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == f"Organization {test_organization["organization_name"]} deleted successfully"
        assert data["data"]["organization_name"] == test_organization["organization_name"]

def test_delete_organization_not_found():
        response = client.delete(
            "/organizations/999",
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Organization not found"

def test_read_my_organizations(test_organization):
        client.post(
            "/organizations/",
            json=test_organization,
            headers={"Authorization": "Bearer test-token"}
        )
        response = client.get(
            "/organizations/my",
            headers={"Authorization": "Bearer test-token"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["message"] == "Organizations retrieved successfully"
        assert isinstance(data["data"], list)

def test_read_my_organizations_unauthorized():
        response = client.get(
            "/organizations/my",
            headers={}
        )
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Not authenticated"
