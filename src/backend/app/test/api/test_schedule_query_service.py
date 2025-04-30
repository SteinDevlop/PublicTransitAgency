"""from fastapi.testclient import TestClient
from backend.app.api.routes.schedule_query_service import app

client = TestClient(app)

def test_list_all_schedules():
    response = client.get("/schedule")
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)

def test_get_schedule_success():
    schedule_id = "test_id"
    response = client.get(f"/schedule/{schedule_id}")
    if response.status_code == 200:
        assert "data" in response.json()
    else:
        assert response.status_code == 404

def test_get_schedules_by_route_success():
    route_id = "test_route"
    response = client.get(f"/schedule/route/{route_id}")
    if response.status_code == 200:
        assert "data" in response.json()
    else:
        assert response.status_code == 404
"""