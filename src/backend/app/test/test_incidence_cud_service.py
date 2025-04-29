"""from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_cud_service import app  
client = TestClient(app)

def test_create_incidence_success(monkeypatch):
    monkeypatch.setattr(
        "app.controller.add",
        lambda data: {**data, "incidence_id": 1}
    )

    response = client.post(
        "/incidence/create",
        data={
            "description": "Rueda pinchada",
            "type": "Mecánico",
            "status": "Pendiente",
            "incidence_id": 1
        }
    )
    assert response.status_code == 200
    body = response.json()
    assert body["operation"] == "create"
    assert body["data"]["incidence_id"] == 1
    assert body["message"] == "Incidencia creada exitosamente"

def test_create_incidence_invalid_data(monkeypatch):
    def raise_value_error(data):
        raise ValueError("Datos inválidos")
    monkeypatch.setattr("app.controller.add", raise_value_error)

    response = client.post(
        "/incidence/create",
        data={
            "description": "Motor roto",
            "type": "Mecánico",
            "status": "Pendiente"
        }
    )
    assert response.status_code == 400
    assert "Datos inválidos" in response.text

def test_update_incidence_success(monkeypatch):
    monkeypatch.setattr(
        "app.controller.get_by_id",
        lambda cls, id: {"incidence_id": id, "description": "Viejo", "type": "Mecánico", "status": "Pendiente"}
    )
    monkeypatch.setattr(
        "app.controller.update",
        lambda data: data
    )

    response = client.post(
        "/incidence/update",
        data={
            "incidence_id": 1,
            "description": "Motor nuevo",
            "type": "Eléctrico",
            "status": "Resuelto"
        }
    )
    assert response.status_code == 200
    body = response.json()
    assert body["operation"] == "update"
    assert body["data"]["description"] == "Motor nuevo"
    assert body["message"] == "Incidencia 1 actualizada"

def test_update_incidence_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.controller.get_by_id",
        lambda cls, id: None
    )

    response = client.post(
        "/incidence/update",
        data={
            "incidence_id": 999,
            "description": "No existe",
            "type": "Desconocido",
            "status": "Inexistente"
        }
    )
    assert response.status_code == 404
    assert "Incidencia no encontrada" in response.text

def test_delete_incidence_success(monkeypatch):
    monkeypatch.setattr(
        "app.controller.get_by_id",
        lambda cls, id: {"incidence_id": id}
    )
    monkeypatch.setattr(
        "app.controller.delete",
        lambda instance: True
    )

    response = client.post(
        "/incidence/delete",
        data={"incidence_id": 1}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["operation"] == "delete"
    assert body["message"] == "Incidencia 1 eliminada"

def test_delete_incidence_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.controller.get_by_id",
        lambda cls, id: None
    )

    response = client.post(
        "/incidence/delete",
        data={"incidence_id": 999}
    )
    assert response.status_code == 404
    assert "Incidencia no encontrada" in response.text
    """