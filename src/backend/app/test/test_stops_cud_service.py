"""import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_cud_service import app, StopCreate, StopOut
client = TestClient(app)

@pytest.fixture
def mock_data():
    return {
        "stop_id": "123",
        "stop_data": {"name": "Stop A", "location": "Location A"}
    }

def test_create_stop(mock_data):
    response = client.post("/stops/create", json=mock_data)
    assert response.status_code == 200
    assert "<h1>Stop Created Successfully</h1>" in response.text
    assert "Stop ID: 123" in response.text
    assert "Message: Stop created successfully" in response.text

def test_update_stop(mock_data):
    response = client.post("/stops/update", json=mock_data)
    assert response.status_code == 200
    assert "<h1>Stop Updated Successfully</h1>" in response.text
    assert "Stop ID: 123" in response.text
    assert "Message: Stop 123 updated" in response.text

def test_delete_stop(mock_data):
    response = client.post("/stops/delete", json=mock_data)
    assert response.status_code == 200
    assert "<h1>Stop Deleted Successfully</h1>" in response.text
    assert "Stop ID: 123" in response.text
    assert "Message: Stop 123 deleted" in response.text

def test_create_stop_missing_stop_id():
    response = client.post("/stops/create", json={"stop_data": {"name": "Stop B", "location": "Location B"}})
    assert response.status_code == 400
    assert "stop_id is required" in response.text

def test_update_stop_not_found():
    response = client.post("/stops/update", json={"stop_id": "999", "stop_data": {"name": "Stop C", "location": "Location C"}})
    assert response.status_code == 404
    assert "Stop not found" in response.text

def test_delete_stop_not_found():
    response = client.post("/stops/delete", json={"stop_id": "999"})
    assert response.status_code == 404
    assert "Stop not found" in response.text
"""