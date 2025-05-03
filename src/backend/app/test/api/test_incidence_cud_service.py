from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.templating import Jinja2Templates
from backend.app.api.routes.incidence_CUD_service import app as incidence_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import IncidenceCreate, IncidenceOut

app_for_test = FastAPI()
app_for_test.include_router(incidence_router)
client = TestClient(app_for_test)
templates = Jinja2Templates(directory="src/backend/app/templates")
controller = UniversalController()


def test_create_incidence_form():
    response = client.get("/incidence/crear")
    assert response.status_code == 200
    assert "Crear Incidencia" in response.text

def test_update_incidence_form():
    response = client.get("/incidence/actualizar")
    assert response.status_code == 200
    assert "Actualizar Incidencia" in response.text

def test_delete_incidence_form():
    response = client.get("/incidence/borrar")
    assert response.status_code == 200
    assert "Borrar Incidencia" in response.text


def test_create_incidence():
    controller.add(IncidenceCreate(IncidenciaID=9, Descripcion="Falla técnica", Tipo="Técnica", TicketID=101))
    response = client.post(
        "/incidence/create",
        data={
            "Descripcion": "Falla en el sistema",
            "Tipo": "Técnica",
            "TicketID": 101
        }
    )
    assert response.status_code == 200



def test_update_incidence_existing():
    controller.add(IncidenceCreate(IncidenciaID=9, Descripcion="Falla técnica", Tipo="Técnica", TicketID=101))
    # Crear una incidencia para actualizar  

    response = client.post(
        "/incidence/update",
        data={
            "IncidenciaID": 1,
            "Descripcion": "Falla corregida",
            "Tipo": "Operativa",
            "TicketID": 103
        }
    )
    assert response.status_code == 200


def test_delete_incidence_existing():
    controller.add(IncidenceCreate(IncidenciaID=9, Descripcion="Falla técnica", Tipo="Técnica", TicketID=101))
    # Crear una incidencia para eliminar

    # Eliminar la incidencia
    response = client.post("/incidence/delete", data={"IncidenciaID": 1})
    assert response.status_code == 200
    