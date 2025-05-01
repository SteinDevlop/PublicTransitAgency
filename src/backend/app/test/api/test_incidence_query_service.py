import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app as incidence_router
from backend.app.logic.universal_controller_sql import UniversalController  # Importa el controlador proporcionado
from backend.app.models.incidence import IncidenceCreate, IncidenceOut
from typing import List, Dict, Any


app = FastAPI()
app.include_router(incidence_router)
client = TestClient(app)


# # Fixture para la sesión de la base de datos de prueba
# @pytest.fixture(scope="function")
# def db():
#     create_tables()
#     yield TestingSessionLocal()
#     clear_tables()

# Fixture para el controlador universal
@pytest.fixture
def controller():
    return UniversalController()  # Utiliza el controlador proporcionado



def test_consultar_incidence_page():
    """Prueba que la ruta '/incidence/consultar' devuelve la plantilla 'ConsultarIncidencia.html' correctamente."""
    response = client.get("/incidence/consultar")
    assert response.status_code == 200
    assert "Consultar Incidencia" in response.text



def test_get_all_incidences(controller: UniversalController):
    """Prueba que la ruta '/incidence/incidencias' devuelve todas las incidencias."""
    # Crear algunas incidencias de prueba usando el controlador
    controller.clear_tables()  # Limpiar la base de datos antes de la prueba
    incidence1 = IncidenceCreate(Descripcion="Incidencia1", Tipo="Tipo1", TicketID=5)
    incidence2 = IncidenceCreate(Descripcion="Incidencia2", Tipo="Tipo2", TicketID=6)
    controller.add(incidence1)
    controller.add(incidence2)

    response = client.get("/incidence/incidencias")
    assert response.status_code == 200
    data: List[Dict[str, Any]] = response.json()
    assert len(data) >= 2
    assert data[0]["Descripcion"] in ["Incidencia1", "Incidencia2"]
    assert data[0]["Tipo"] in ["Tipo1", "Tipo2"]
    assert data[0]["TicketID"] in [5, 6]



def test_get_incidence_by_id_existing(controller: UniversalController):
    """Prueba que la ruta '/incidence/incidencia/{IncidenciaID}' devuelve la incidencia correcta cuando existe."""
    controller.clear_tables() # Clear table
    # Crear una incidencia de prueba usando el controlador
    incidence_create = IncidenceCreate(Descripcion="FindByIDE", Tipo="TipoIDE", TicketID=7)
    created_incidence = controller.add(incidence_create)
    incidence_id = created_incidence.IncidenciaID

    response = client.get(f"/incidence/incidencia/{incidence_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["Descripcion"] == "FindByIDE"
    assert data["Tipo"] == "TipoIDE"
    assert data["TicketID"] == 7



def test_get_incidence_by_id_not_found():
    """Prueba que la ruta '/incidence/incidencia/{IncidenciaID}' devuelve un error 404 cuando no encuentra la incidencia."""
    response = client.get("/incidence/incidencia/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia not found"
