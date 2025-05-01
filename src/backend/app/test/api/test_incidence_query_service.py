import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app as incidence_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import IncidenceCreate, IncidenceOut
from typing import List, Dict, Any

# Crear una instancia de la aplicación FastAPI para las pruebas
app_for_test = FastAPI()
app_for_test.include_router(incidence_router)
client = TestClient(app_for_test)

# Fixture para el controlador universal
@pytest.fixture
def controller():
    return UniversalController()

def test_consultar_page_incidence():
    """Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarIncidencia.html' correctamente."""
    response = client.get("/incidence/consultar")
    assert response.status_code == 200
    assert "Consultar Incidencia" in response.text

def test_get_all_incidences(controller: UniversalController):
    """Prueba que la ruta '/incidencias' devuelve correctamente todas las incidencias."""
    # Limpiar la base de datos antes de la prueba
    controller.clear_tables()

    # Crear algunas incidencias de prueba usando el controlador
    incidence1 = IncidenceCreate(Descripcion="Incidencia1", Tipo="Tipo1", TicketID=5)
    incidence2 = IncidenceCreate(Descripcion="Incidencia2", Tipo="Tipo2", TicketID=6)
    controller.add(incidence1)
    controller.add(incidence2)

    response = client.get("/incidence/incidencias")
    assert response.status_code == 200
    data: List[Dict[str, Any]] = response.json()
    assert len(data) >= 2
    # Verificar que los datos devueltos coinciden con los creados
    assert any(d["Descripcion"] == "Incidencia1" and d["Tipo"] == "Tipo1" and d["TicketID"] == 5 for d in data)
    assert any(d["Descripcion"] == "Incidencia2" and d["Tipo"] == "Tipo2" and d["TicketID"] == 6 for d in data)



def test_get_incidence_by_id_existing(controller: UniversalController):
    """Prueba que la ruta '/incidencia/{IncidenciaID}' devuelve la incidencia correcta cuando existe."""
    # Limpiar la base de datos antes de la prueba
    controller.clear_tables()
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
    """Prueba que la ruta '/incidencia/{IncidenciaID}' devuelve un error 404 cuando no encuentra la incidencia."""
    response = client.get("/incidence/incidencia/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia not found"
