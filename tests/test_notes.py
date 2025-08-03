import pytest
from .conftest import (setup_database, teardown_database, client,
                       headers, test_organization, test_channel, test_topic, test_user)


@pytest.fixture(autouse=True)
def setup():
    setup_database()
    yield
    teardown_database()

@pytest.fixture
def test_note_text(test_topic):
    return {
        "title": "Test Note",
        "content_type": "text",
        "content": "This is a test note.",
        "topic_id": 1,
        "organization_id": 1,
        "user_id": 1
    }

@pytest.fixture
def test_note_image(test_topic):
    return {
        "title": "Test Note with Image",
        "content_type": "image",
        "content": "http://example.com/image.jpg",
        "topic_id": 1,
        "organization_id": 1,
        "user_id": 1
    }


def test_read_my_notes(headers, test_organization, test_channel, test_topic, test_note_text):
    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/", json=test_channel, headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/", json=test_topic, headers=headers)
    assert response.status_code == 200

    response = client.post("/notes/", data=test_note_text, headers=headers)
    assert response.status_code == 200

    response = client.get("/notes/my", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Your notes retrieved successfully"
    assert isinstance(data["data"], list)

def test_read_my_notes_no_notes(headers):
    response = client.get("/notes/my", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No notes found for this user"

def test_read_my_notes_no_auth():
    response = client.get("/notes/my")
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Not authenticated"

def test_read_notes_in_topic(headers, test_organization, test_channel, test_topic, test_note_text):
    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/", json=test_channel, headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/", json=test_topic, headers=headers)
    assert response.status_code == 200

    response = client.post("/notes/", data=test_note_text, headers=headers)
    assert response.status_code == 200

    response = client.get("/notes/notes_in_topic?topic_id=1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Notes retrieved successfully"
    assert isinstance(data["data"], list)

def test_read_notes_in_topic_no_notes(headers, test_topic):
    response = client.get("/notes/notes_in_topic?topic_id=1", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No notes found in this topic"

def test_give_like(headers, test_organization, test_channel, test_topic, test_note_text, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201
    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/", json=test_channel, headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/", json=test_topic, headers=headers)
    assert response.status_code == 200

    form_data = {
        "title": test_note_text["title"],
        "content_type": test_note_text["content_type"],
        "content": test_note_text["content"],
        "topic_id": test_note_text["topic_id"],
        "organization_id": test_note_text["organization_id"]
    }
    response = client.post("/notes/", data=form_data, headers=headers)
    assert response.status_code == 200

    response = client.post("/notes/give_like?note_id=1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Note has been liked"
    assert data["data"]["likes"] == 1
    assert data["data"]["author_score"] == 1
    assert data["data"]["author_rank"] == "niekompetentny"

def test_give_like_already_liked(headers, test_organization, test_channel, test_topic, test_note_text, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/", json=test_channel, headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/", json=test_topic, headers=headers)
    assert response.status_code == 200

    form_data = {
        "title": test_note_text["title"],
        "content_type": test_note_text["content_type"],
        "content": test_note_text["content"],
        "topic_id": test_note_text["topic_id"],
        "organization_id": test_note_text["organization_id"]
    }
    response = client.post("/notes/", data=form_data, headers=headers)
    assert response.status_code == 200

    response = client.post("/notes/give_like?note_id=1", headers=headers)
    assert response.status_code == 200

    response = client.post("/notes/give_like?note_id=1", headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "You have already like/disliked this note"

def test_give_dislike(headers, test_organization, test_channel, test_topic, test_note_text, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/", json=test_channel, headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/", json=test_topic, headers=headers)
    assert response.status_code == 200

    form_data = {
        "title": test_note_text["title"],
        "content_type": test_note_text["content_type"],
        "content": test_note_text["content"],
        "topic_id": test_note_text["topic_id"],
        "organization_id": test_note_text["organization_id"]
    }
    response = client.post("/notes/", data=form_data, headers=headers)
    assert response.status_code == 200

    response = client.post("/notes/give_dislike?note_id=1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Note has been disliked"
    assert data["data"]["likes"] == -1
    assert data["data"]["author_score"] == -1
    assert data["data"]["author_rank"] == "niekompetentny"

def test_give_dislike_already_disliked(headers, test_organization, test_channel, test_topic, test_note_text, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/", json=test_channel, headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/", json=test_topic, headers=headers)
    assert response.status_code == 200

    form_data = {
        "title": test_note_text["title"],
        "content_type": test_note_text["content_type"],
        "content": test_note_text["content"],
        "topic_id": test_note_text["topic_id"],
        "organization_id": test_note_text["organization_id"]
    }
    response = client.post("/notes/", data=form_data, headers=headers)
    assert response.status_code == 200

    response = client.post("/notes/give_dislike?note_id=1", headers=headers)
    assert response.status_code == 200

    response = client.post("/notes/give_dislike?note_id=1", headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "You have already like/disliked this note"

def test_read_notes(headers, test_organization, test_channel, test_topic, test_note_text):
    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/", json=test_channel, headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/", json=test_topic, headers=headers)
    assert response.status_code == 200

    form_data = {
        "title": test_note_text["title"],
        "content_type": test_note_text["content_type"],
        "content": test_note_text["content"],
        "topic_id": test_note_text["topic_id"],
        "organization_id": test_note_text["organization_id"]
    }
    response = client.post("/notes/", data=form_data, headers=headers)
    assert response.status_code == 200

    response = client.get("/notes/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Notes retrieved successfully"
    assert isinstance(data["data"], list)

def test_read_notes_no_notes(headers):
    response = client.get("/notes/", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No notes found"

def test_read_note(headers, test_organization, test_channel, test_topic, test_note_text):
    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/", json=test_channel, headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/", json=test_topic, headers=headers)
    assert response.status_code == 200

    form_data = {
        "title": test_note_text["title"],
        "content_type": test_note_text["content_type"],
        "content": test_note_text["content"],
        "topic_id": test_note_text["topic_id"],
        "organization_id": test_note_text["organization_id"]
    }
    response = client.post("/notes/", data=form_data, headers=headers)
    assert response.status_code == 200

    response = client.get("/notes/1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Note retrieved successfully"
    assert data["data"]["title"] == test_note_text["title"]

def test_read_note_no_note(headers):
    response = client.get("/notes/1", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No notes found"

def test_create_note_text(headers, test_organization, test_channel, test_topic, test_note_text):
    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/", json=test_channel, headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/", json=test_topic, headers=headers)
    assert response.status_code == 200

    form_data = {
        "title": test_note_text["title"],
        "content_type": test_note_text["content_type"],
        "content": test_note_text["content"],
        "topic_id": test_note_text["topic_id"],
        "organization_id": test_note_text["organization_id"]
    }
    response = client.post("/notes/", data=form_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Note created successfully"
    assert data["data"]["title"] == test_note_text["title"]

def test_create_note_image(headers, test_organization, test_channel, test_topic, test_note_image):
    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/", json=test_channel, headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/", json=test_topic, headers=headers)
    assert response.status_code == 200

    form_data = {
        "title": test_note_image["title"],
        "content_type": test_note_image["content_type"],
        "content": test_note_image["content"],
        "topic_id": test_note_image["topic_id"],
        "organization_id": test_note_image["organization_id"]
    }
    response = client.post("/notes/", data=form_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Note created successfully"
    assert data["data"]["title"] == test_note_image["title"]

def test_create_note_no_auth(test_note_text):
    form_data = {
        "title": test_note_text["title"],
        "content_type": test_note_text["content_type"],
        "content": test_note_text["content"],
        "topic_id": test_note_text["topic_id"],
        "organization_id": test_note_text["organization_id"]
    }
    response = client.post("/notes/", data=form_data)
    assert response.status_code == 401
    data = response.json()
    assert data["detail"] == "Not authenticated"


def test_delete_note(headers, test_organization, test_channel, test_topic, test_note_text):
    response = client.post("/organizations/", json=test_organization, headers=headers)
    assert response.status_code == 200

    response = client.post("/channels/", json=test_channel, headers=headers)
    assert response.status_code == 200

    response = client.post("/topics/", json=test_topic, headers=headers)
    assert response.status_code == 200

    form_data = {
        "title": test_note_text["title"],
        "content_type": test_note_text["content_type"],
        "content": test_note_text["content"],
        "topic_id": test_note_text["topic_id"],
        "organization_id": test_note_text["organization_id"]
    }
    response = client.post("/notes/", data=form_data, headers=headers)
    assert response.status_code == 200

    response = client.delete("/notes/1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Note deleted successfully"

def test_delete_note_not_found(headers):
    response = client.delete("/notes/999", headers=headers)
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Note not found"
