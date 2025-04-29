"""from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app  
client = TestClient(app)

def test_list_incidences_json(monkeypatch):
    monkeypatch.setattr(
        "app.controller.read_all",
        lambda cls: [
            {"incidence_id": 1, "description": "Rueda pinchada", "type": "Mecánico", "status": "Pendiente"},
            {"incidence_id": 2, "description": "Motor dañado", "type": "Mecánico", "status": "Resuelto"}
        ]
    )

    response = client.get("/incidence/list", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)

def test_list_incidences_html(monkeypatch):
    monkeypatch.setattr(
        "app.controller.read_all",
        lambda cls: [
            {"incidence_id": 1, "description": "Puerta rota", "type": "Mecánico", "status": "Pendiente"}
        ]
    )

    response = client.get("/incidence/list", headers={"Accept": "text/html"})
    assert response.status_code == 200
    assert "<table" in response.text
    assert "Puerta rota" in response.text
    assert "Mecánico" in response.text

def test_get_incidence_success(monkeypatch):
    monkeypatch.setattr(
        "app.controller.get_by_id",
        lambda cls, id: {"incidence_id": id, "description": "Motor quemado", "type": "Eléctrico", "status": "Pendiente"}
    )

    response = client.get("/incidence/1", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert "data" in response.json()
    assert response.json()["data"]["incidence_id"] == 1

def test_get_incidence_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.controller.get_by_id",
        lambda cls, id: None
    )

    response = client.get("/incidence/999", headers={"Accept": "application/json"})
    assert response.status_code == 404
    assert "Incidencia no encontrada" in response.text

def test_get_by_unit_transport(monkeypatch):
    mock_data = [
        {"unit_transport_id": 1, "description": "Aire acondicionado dañado", "type": "Confort", "status": "Pendiente"},
        {"unit_transport_id": 2, "description": "Parabrisas roto", "type": "Mecánico", "status": "Pendiente"},
    ]

    monkeypatch.setattr(
        "app.controller.read_all",
        lambda cls: mock_data
    )

    response = client.get("/incidence/unit_transport/1", headers={"Accept": "application/json"})
    assert response.status_code == 200
    assert response.json()["data"][0]["unit_transport_id"] == 1

def test_get_by_unit_transport_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.controller.read_all",
        lambda cls: []
    )

    response = client.get("/incidence/unit_transport/123", headers={"Accept": "application/json"})
    assert response.status_code == 404
    assert "No se encontraron incidencias" in response.text
"""