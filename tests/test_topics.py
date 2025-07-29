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

def test_read_topics_in_channel(headers, test_organization, test_channel, test_topic):
    response = client.post("/organizations/",
                         json=test_organization,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/",
                         json=test_channel,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/",
                         json=test_topic,
                         headers=headers)
    assert response.status_code == 200

    response = client.get("/topics/topics_in_channel?channel_id=1",
                        headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Topics retrieved successfully"
    assert isinstance(data["data"], list)

def test_read_topics_in_channel_not_found(headers):
    response = client.get("/topics/topics_in_channel?channel_id=999",
                        headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No topics found in this channel"

def test_read_topics_in_channel_invalid_channel(headers):
    response = client.get("/topics/topics_in_channel?channel_id=abc",
                        headers=headers)
    assert response.status_code == 422


def test_read_topics(headers, test_organization, test_channel, test_topic):
    response = client.post("/organizations/",
                         json=test_organization,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/",
                         json=test_channel,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/",
                         json=test_topic,
                         headers=headers)
    assert response.status_code == 200

    response = client.get("/topics/",
                        headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Topics retrieved successfully"
    assert isinstance(data["data"], list)

def test_read_topics_not_found(headers):
    response = client.get("/topics/",
                        headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No topics found"

def test_read_topics_invalid(headers):
    response = client.get("/topics/invalid_id",
                        headers=headers)
    assert response.status_code == 422

def test_read_topic(headers, test_organization, test_channel, test_topic):
    response = client.post("/organizations/",
                         json=test_organization,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/",
                         json=test_channel,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/",
                         json=test_topic,
                         headers=headers)
    assert response.status_code == 200

    response = client.get(f"/topics/1",
                        headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Topic retrieved successfully"
    assert data["data"]["topic_name"] == test_topic["topic_name"]

def test_read_topic_not_found(headers):
    response = client.get("/topics/999",
                        headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No topic found"

def test_create_topic(headers, test_organization, test_channel, test_topic):
    response = client.post("/organizations/",
                         json=test_organization,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/",
                         json=test_channel,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/",
                         json=test_topic,
                         headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Topic created successfully"
    assert data["data"]["topic_name"] == test_topic["topic_name"]

def test_create_topic_already_exists(headers, test_organization, test_channel, test_topic):
    response = client.post("/organizations/",
                         json=test_organization,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/",
                         json=test_channel,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/",
                         json=test_topic,
                         headers=headers)
    assert response.status_code == 200

    # Attempt to create the same topic again
    response = client.post("/topics/",
                         json=test_topic,
                         headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Topic with this name already exists"

def test_create_topic_invalid_organization(headers, test_channel, test_topic, test_organization):
    client.post("/organizations/",
                json=test_organization,
                headers=headers)
    response = client.post("/channels/",
                         json=test_channel,
                         headers=headers)
    assert response.status_code == 200

    invalid_topic = test_topic.copy()
    invalid_topic["organization_id"] = 999

    response = client.post("/topics/",
                         json=invalid_topic,
                         headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Organization not found"

def test_create_topic_invalid_channel(headers, test_organization, test_topic):
    response = client.post("/organizations/",
                         json=test_organization,
                         headers=headers)
    assert response.status_code == 200

    # Attempt to create a topic with a non-existent channel
    invalid_topic = test_topic.copy()
    invalid_topic["channel_id"] = 999

    response = client.post("/topics/",
                         json=invalid_topic,
                         headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Channel not found"

def test_create_topic_invalid_request(headers, test_organization, test_channel):
    response = client.post("/organizations/",
                         json=test_organization,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/",
                         json=test_channel,
                         headers=headers)
    assert response.status_code == 200

    # Attempt to create a topic with missing fields
    invalid_topic = {
        "topic_name": "Invalid Topic",
        "channel_id": 1
        # Missing organization_id
    }

    response = client.post("/topics/",
                         json=invalid_topic,
                         headers=headers)
    assert response.status_code == 422

def test_create_topic_invalid_json(headers, test_organization, test_channel):
    response = client.post("/organizations/",
                         json=test_organization,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/",
                         json=test_channel,
                         headers=headers)
    assert response.status_code == 200

    # Attempt to create a topic with invalid JSON
    response = client.post("/topics/",
                         data="invalid_json",
                         headers=headers)
    assert response.status_code == 422

def test_create_topic_unauthorized(headers, test_organization, test_channel, test_topic):
    # Remove the authorization header to simulate unauthorized access
    unauthorized_headers = {}

    response = client.post("/organizations/",
                         json=test_organization,
                         headers=unauthorized_headers)
    assert response.status_code == 401

    response = client.post("/channels/",
                         json=test_channel,
                         headers=unauthorized_headers)
    assert response.status_code == 404

    response = client.post("/topics/",
                         json=test_topic,
                         headers=unauthorized_headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Organization not found"

def test_delete_topic(headers, test_organization, test_channel, test_topic):
    response = client.post("/organizations/",
                         json=test_organization,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/",
                         json=test_channel,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/",
                         json=test_topic,
                         headers=headers)
    assert response.status_code == 200

    # Delete the topic
    response = client.delete("/topics/1",
                            headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Topic deleted successfully"

def test_delete_topic_not_found(headers):
    response = client.delete("/topics/999",
                            headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Topic not found"

def test_delete_topic_invalid(headers):
    response = client.delete("/topics/invalid_id",
                            headers=headers)
    assert response.status_code == 422

def test_update_topic(headers, test_organization, test_channel, test_topic):
    response = client.post("/organizations/",
                         json=test_organization,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/",
                         json=test_channel,
                         headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/",
                         json=test_topic,
                         headers=headers)
    assert response.status_code == 200

    # Update the topic
    updated_topic = {
        "topic_name": "Updated Test Topic",
        "channel_id": 1,
        "organization_id": 1
    }

    response = client.put("/topics/1",
                        json=updated_topic,
                        headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Topic updated successfully"
    assert data["data"]["topic_name"] == updated_topic["topic_name"]

def test_update_topic_not_found(headers):
    updated_topic = {
        "topic_name": "Updated Test Topic",
        "channel_id": 1,
        "organization_id": 1
    }

    response = client.put("/topics/999",
                        json=updated_topic,
                        headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Topic not found"

def test_update_topic_invalid(headers):
    updated_topic = {
        "topic_name": "Updated Test Topic",
        "channel_id": 1,
        "organization_id": 1
    }

    response = client.put("/topics/invalid_id",
                        json=updated_topic,
                        headers=headers)
    assert response.status_code == 422


