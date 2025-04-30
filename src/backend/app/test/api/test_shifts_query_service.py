"""from fastapi.testclient import TestClient
from backend.app.api.routes.shifts_query_service import app
client = TestClient(app)

def test_get_all_shifts():
    response = client.get("/shift")
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

def test_get_shift_by_id():
    shift_id = "SHIFT001"
    response = client.get(f"/shift/{shift_id}")
    if response.status_code == 200:
        assert "data" in response.json()
        assert response.json()["data"]["shift_id"] == shift_id
    elif response.status_code == 404:
        assert response.json()["detail"] == "Shift not found"

def test_get_shifts_by_driver():
    driver_id = "DRIVER001"
    response = client.get(f"/shift/driver/{driver_id}")
    if response.status_code == 200:
        assert "data" in response.json()
        assert all(s["driver_id"] == driver_id for s in response.json()["data"])
    elif response.status_code == 404:
        assert response.json()["detail"] == "No shifts found for this driver"

def test_get_shifts_by_unit():
    unit_id = "UNIT001"
    response = client.get(f"/shift/unit/{unit_id}")
    if response.status_code == 200:
        assert "data" in response.json()
        assert all(s["unit_id"] == unit_id for s in response.json()["data"])
    elif response.status_code == 404:
        assert response.json()["detail"] == "No shifts found for this unit"
"""