"""import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_cud_service import app
client = TestClient(app)

def test_get_all_stops():
    response = client.get("/stops")
    assert response.status_code == 200
    assert "<h1>All Stops</h1>" in response.text

def test_get_stop():
    response = client.get("/stops/some_stop_id")
    assert response.status_code == 200
    assert "<h1>Stop Details</h1>" in response.text
    assert "<strong>Name:</strong>" in response.text
    assert "<strong>Location:</strong>" in response.text

def test_get_stop_not_found():
    response = client.get("/stops/non_existing_id")
    assert response.status_code == 404
    assert "Stop not found" in response.text

def test_search_stops_by_name():
    response = client.get("/stops/search?name=some_stop_name")
    assert response.status_code == 200
    assert "<h1>Search Results</h1>" in response.text
    assert "<li>" in response.text

def test_search_stops_by_location():
    response = client.get("/stops/search?location=some_location")
    assert response.status_code == 200
    assert "<h1>Search Results</h1>" in response.text
    assert "<li>" in response.text

def test_search_stops_no_results():
    response = client.get("/stops/search?name=non_existing_name")
    assert response.status_code == 200
    assert "<h1>No Stops Found</h1>" in response.text
"""