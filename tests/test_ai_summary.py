import pytest
from .conftest import setup_database, teardown_database, client


@pytest.fixture(autouse=True)
def setup():
    setup_database()
    yield
    teardown_database()


def test_create_ai_summary(test_topic, test_channel, test_organization, headers):
    response = client.post("/organizations/",
                           json=test_organization, headers=headers)
    assert response.status_code == 200
    response = client.post("/channels/",
                           json=test_channel, headers=headers)
    assert response.status_code == 200
    response = client.post("/topics/",
                           json=test_topic, headers=headers)
    assert response.status_code == 200
    response = client.post("/ai_summary/?topic_id=1",
                            headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "AI Summary created successfully"
    assert isinstance(data["data"], dict)

def test_get_ai_summary(headers, test_topic, test_channel, test_organization):
    response = client.post("/organizations/",
                          json=test_organization, headers=headers)
    assert response.status_code == 200
    response = client.post("/channels/",
                          json=test_channel, headers=headers)
    assert response.status_code == 200
    response = client.post("/topics/",
                          json=test_topic, headers=headers)
    assert response.status_code == 200
    response = client.post("/ai_summary/?topic_id=1",
                          headers=headers)
    assert response.status_code == 200
    response = client.get("/ai_summary/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "AI summaries retrieved successfully"
    assert isinstance(data["data"], list)
    assert len(data["data"]) > 0
    assert isinstance(data["data"][0], dict)

def test_update_ai_summary(headers, test_topic, test_channel, test_organization):
    response = client.post("/organizations/",
                          json=test_organization, headers=headers)
    assert response.status_code == 200
    response = client.post("/channels/",
                          json=test_channel, headers=headers)
    assert response.status_code == 200
    response = client.post("/topics/",
                          json=test_topic, headers=headers)
    assert response.status_code == 200
    response = client.post("/ai_summary/?topic_id=1",
                          headers=headers)
    assert response.status_code == 200
    response = client.put(f"/ai_summary/1?topic_id=1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "AI Summary updated successfully"
    assert isinstance(data["data"], dict)

def test_delete_ai_summary(headers, test_topic, test_channel, test_organization):
    response = client.post("/organizations/",
                          json=test_organization, headers=headers)
    assert response.status_code == 200
    response = client.post("/channels/",
                          json=test_channel, headers=headers)
    assert response.status_code == 200
    response = client.post("/topics/",
                          json=test_topic, headers=headers)
    assert response.status_code == 200
    response = client.post("/ai_summary/?topic_id=1",
                          headers=headers)
    assert response.status_code == 200
    response = client.delete("/ai_summary/1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "AI Summary deleted successfully"
    assert data["data"] is None