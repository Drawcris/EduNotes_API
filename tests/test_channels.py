import pytest
from .conftest import setup_database, teardown_database, client, test_channel, test_organization

@pytest.fixture(autouse=True)
def setup_and_teardown():
    setup_database()
    yield
    teardown_database()


def test_read_channels(test_channel, test_organization):
    client.post(
        '/organizations/',
        json=test_organization,
        headers={"Authorization": "Bearer test-token"}
    )
    client.post(
        '/channels/',
        json=test_channel,
        headers={"Authorization": "Bearer test-token"}
    )
    response = client.get('/channels/',
                          headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Channels retrieved successfully"
    assert isinstance(data["data"], list)

def test_read_channel(test_channel, test_organization):
    client.post(
        '/organizations/',
        json=test_organization,
        headers={"Authorization": "Bearer test-token"}
    )
    client.post(
        '/channels/',
        json=test_channel,
        headers={"Authorization": "Bearer test-token"}
    )
    response = client.get('/channels/1/',
                          headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == 'Channel retrieved successfully'
    assert data["data"]["channel_name"] == test_channel["channel_name"]

def test_read_channel_not_found(test_organization):
    client.post(
        '/organizations/',
        json=test_organization,
        headers={"Authorization": "Bearer test-token"}
    )
    response = client.get('/channels/999/',
                            headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == 'Channel not found'

def test_create_channel(test_channel, test_organization):
    client.post(
        '/organizations/',
        json=test_organization,
        headers={"Authorization": "Bearer test-token"})
    response = client.post(
        '/channels/',
        json=test_channel,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Channel created successfully"
    assert data["data"]["channel_name"] == test_channel["channel_name"]

def test_delete_channel(test_channel, test_organization):
    client.post(
        '/organizations/',
        json=test_organization,
        headers={"Authorization": "Bearer test-token"}
    )
    client.post(
        '/channels/',
        json=test_channel,
        headers={"Authorization": "Bearer test-token"}
    )
    response = client.delete(
        '/channels/1/',
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Channel deleted successfully"
    assert data["data"]["channel_name"] == test_channel["channel_name"]

def test_delete_channel_not_found(test_organization):
    client.post(
        '/organizations/',
        json=test_organization,
        headers={"Authorization": "Bearer test-token"}
    )
    response = client.delete(
        '/channels/999/',
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == 'Channel not found'

def test_update_channel(test_channel, test_organization):
    client.post(
        '/organizations/',
        json=test_organization,
        headers={"Authorization": "Bearer test-token"}
    )
    client.post(
        '/channels/',
        json=test_channel,
        headers
        ={"Authorization": "Bearer test-token"}
    )
    updated_channel = {
        "channel_name": "Updated Channel",
        "organization_id": 1,
    }
    response = client.put(
        '/channels/1/',
        json=updated_channel,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Channel updated successfully"
    assert data["data"]["channel_name"] == updated_channel["channel_name"]

def test_update_channel_not_found(test_organization):
    client.post(
        '/organizations/',
        json=test_organization,
        headers={"Authorization": "Bearer test-token"}
    )
    updated_channel = {
        "channel_name": "Updated Channel",
        "organization_id": 1,
    }
    response = client.put(
        '/channels/999/',
        json=updated_channel,
        headers={"Authorization": "Bearer test-token"}
    )
    assert response.status_code == 404
    data = response.json()
    assert data['detail'] == 'Channel not found'


