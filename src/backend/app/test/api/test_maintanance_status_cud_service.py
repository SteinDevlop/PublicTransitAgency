"""from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_CUD_service import app as status_router

app_for_test = FastAPI()
app_for_test.include_router(status_router)
client = TestClient(app_for_test)

def test_create_status():
    response = client.post(
        "/maintainance_status/create",
        data={"TipoEstado": "Nuevo", "UnidadTransporte": "Unidad-X", "Status": "Activo"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["operation"] == "create"
    assert data["data"]["TipoEstado"] == "Nuevo"
    assert data["data"]["UnidadTransporte"] == "Unidad-X"
    assert data["data"]["Status"] == "Activo"

def test_update_status_existing():
    # Primero, crear un estado para actualizar
    create_response = client.post(
        "/maintainance_status/create",
        data={"TipoEstado": "Original", "UnidadTransporte": "Unidad-Y", "Status": "Inactivo"}
    )
    assert create_response.status_code == 200
    created_data = create_response.json()["data"]
    created_id = created_data["ID"]

    response = client.post(
        "/maintainance_status/update",
        data={
            "ID": created_id,
            "TipoEstado": "Actualizado",
            "UnidadTransporte": "Unidad-Z",
            "Status": "Activo"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["operation"] == "update"
    assert data["data"]["TipoEstado"] == "Actualizado"
    assert data["data"]["UnidadTransporte"] == "Unidad-Z"
    assert data["data"]["Status"] == "Activo"

def test_update_status_not_found():
    response = client.post(
        "/maintainance_status/update",
        data={"ID": 9999, "TipoEstado": "NonExistent", "UnidadTransporte": "None", "Status": "None"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Maintainance status not found"

def test_delete_status_existing():
    # Primero, crear un estado para eliminar
    create_response = client.post(
        "/maintainance_status/create",
        data={"TipoEstado": "ToDelete", "UnidadTransporte": "Unidad-W", "Status": "Activo"}
    )
    assert create_response.status_code == 200
    created_data = create_response.json()["data"]
    deleted_id = created_data["ID"]
    response = client.post("/maintainance_status/delete", data={"ID": deleted_id})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["operation"] == "delete"

def test_delete_status_not_found():
    response = client.post("/maintainance_status/delete", data={"ID": 9999})
    assert response.status_code == 404
    assert response.json()["detail"] == "Maintainance status not found"

def test_index_create_form():
    response = client.get("/maintainance_status/crear")
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/maintainance_status/actualizar")
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/maintainance_status/eliminar")
    assert response.status_code == 200
    """