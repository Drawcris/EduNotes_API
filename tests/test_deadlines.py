import pytest
from .conftest import setup_database, teardown_database, client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    setup_database()
    yield
    teardown_database()


@pytest.fixture
def test_deadline_assignment():
    return {
        "event_type": "Zadanie",
        "event_name": "Test Event Name",
        "event_description": "Test Event Description",
        "event_date": "2023-10-01T00:00:00Z",
        "organization_id": 1,
    }

@pytest.fixture
def test_deadline_exam():
    return {
        "event_type": "Egzamin",
        "event_name": "Test Exam Name",
        "event_description": "Test Exam Description",
        "event_date": "2023-10-01T00:00:00Z",
        "organization_id": 1,
    }

def test_read_deadlines(test_deadline_exam):
    client.post("/deadlines/",
                data=test_deadline_exam,
                headers={"Authorization": "Bearer test_token"})
    response = client.get("/deadlines/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Deadlines retrieved successfully"
    assert isinstance(data["data"], list)

def test_read_deadlines_empty():
    response = client.get("/deadlines/")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "No deadlines found"

def test_read_deadline(test_deadline_exam):
    client.post("/deadlines/",
                data=test_deadline_exam,
                headers={"Authorization": "Bearer test_token"})
    response = client.get("/deadlines/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Deadline retrieved successfully"
    assert data["data"]["event_type"] == "Egzamin"

def test_read_deadline_not_found():
    response = client.get("/deadlines/999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Deadline not found"

def test_create_deadline_exam(test_deadline_exam):
    response = client.post("/deadlines/",
                           data=test_deadline_exam,
                           headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Deadline created successfully"
    assert data["data"]["event_type"] == "Egzamin"

def test_create_deadline_assignment(test_deadline_assignment):
    response = client.post("/deadlines/",
                           data=test_deadline_assignment,
                           headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Deadline created successfully"
    assert data["data"]["event_type"] == "Zadanie"

def test_create_deadline_invalid_event_type():
    invalid_deadline = {
        "event_type": "InvalidType",
        "event_name": "Invalid Event Name",
        "event_description": "Invalid Event Description",
        "event_date": "2023-10-01T00:00:00Z",
        "organization_id": 1,
    }
    response = client.post("/deadlines/",
                           data=invalid_deadline,
                           headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["msg"] == "Input should be 'Egzamin' or 'Zadanie'"

def test_update_deadline(test_deadline_exam):
    client.post("/deadlines/",
                data=test_deadline_exam,
                headers={"Authorization": "Bearer test_token"})
    update_data = {
        "event_type": "Egzamin",
        "event_name": "Updated Exam Name",
        "event_description": "Updated Exam Description",
        "event_date": "2023-10-02T00:00:00Z",
    }
    response = client.put("/deadlines/1",
                          data=update_data,
                          headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Deadline updated successfully"
    assert data["data"]["event_name"] == "Updated Exam Name"

def test_update_deadline_not_found():
    update_data = {
        "event_type": "Egzamin",
        "event_name": "Updated Exam Name",
        "event_description": "Updated Exam Description",
        "event_date": "2023-10-02T00:00:00Z",
    }
    response = client.put("/deadlines/999",
                          data=update_data,
                          headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Deadline not found"

def test_delete_deadline(test_deadline_exam):
    client.post("/deadlines/",
                data=test_deadline_exam,
                headers={"Authorization": "Bearer test_token"})
    response = client.delete("/deadlines/1",
                             headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Deadline deleted successfully"

def test_delete_deadline_not_found():
    response = client.delete("/deadlines/999",
                             headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Deadline not found"



