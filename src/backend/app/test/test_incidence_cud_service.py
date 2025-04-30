from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.templating import Jinja2Templates
from backend.app.api.routes.incidence_cud_service import app as incidence_router

app_for_test = FastAPI()
app_for_test.include_router(incidence_router)
client = TestClient(app_for_test)
templates = Jinja2Templates(directory="src/backend/app/templates")


def test_create_incidence_form():
    """Prueba que la ruta '/incidence/crear' devuelve el formulario 'CrearIncidencia.html' correctamente."""
    response = client.get("/incidence/crear")
    assert response.status_code == 200
    assert "Crear Incidencia" in response.text

def test_update_incidence_form():
    """Prueba que la ruta '/incidence/actualizar' devuelve el formulario 'ActualizarIncidencia.html' correctamente."""
    response = client.get("/incidence/actualizar")
    assert response.status_code == 200
    assert "Actualizar Incidencia" in response.text

def test_delete_incidence_form():
    """Prueba que la ruta '/incidence/borrar' devuelve el formulario 'BorrarIncidencia.html' correctamente."""
    response = client.get("/incidence/borrar")
    assert response.status_code == 200
    assert "Borrar Incidencia" in response.text

def test_create_incidence():
    response = client.post(
        "/incidence/create",
        data={"Descripcion": "Incidencia de prueba", "Tipo": "Tipo prueba", "TicketID": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["operation"] == "create"
    assert data["data"]["Descripcion"] == "Incidencia de prueba"
    assert data["data"]["Tipo"] == "Tipo prueba"
    assert data["data"]["TicketID"] == 1


def test_update_incidence_existing():
    # Primero, crear una incidencia para actualizar
    create_response = client.post(
        "/incidence/create",
        data={"Descripcion": "Original", "Tipo": "TipoOriginal", "TicketID": 2}
    )
    assert create_response.status_code == 200
    created_data = create_response.json()["data"]
    created_id = created_data["IncidenciaID"]

    response = client.post(
        "/incidence/update",
        data={
            "IncidenciaID": created_id,
            "Descripcion": "Actualizada",
            "Tipo": "TipoActualizado",
            "TicketID": 3
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["operation"] == "update"
    assert data["data"]["Descripcion"] == "Actualizada"
    assert data["data"]["Tipo"] == "TipoActualizado"
    assert data["data"]["TicketID"] == 3


def test_update_incidence_not_found():
    response = client.post(
        "/incidence/update",
        data={"IncidenciaID": 9999, "Descripcion": "NonExistent", "Tipo": "None", "TicketID": 0}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidence not found"



def test_delete_incidence_existing():
    # Primero, crear una incidencia para eliminar
    create_response = client.post(
        "/incidence/create",
        data={"Descripcion": "ToDelete", "Tipo": "TipoDelete", "TicketID": 4}
    )
    assert create_response.status_code == 200
    created_data = create_response.json()["data"]
    deleted_id = created_data["IncidenciaID"]
    response = client.post("/incidence/delete", data={"IncidenciaID": deleted_id})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["operation"] == "delete"


def test_delete_incidence_not_found():
    response = client.post("/incidence/delete", data={"IncidenciaID": 9999})
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidence not found"
