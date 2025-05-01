from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app as incidences_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence, IncidenceCreate, IncidenceOut
from typing import List, Dict, Any

client = TestClient(incidences_router)

# Limpieza de base de datos antes y después de cada test
def setup_function():
    """Limpia las tablas antes de cada prueba."""
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(incidences_router)

def test_consultar_page_incidence():
    """Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarIncidencia.html' correctamente."""
    response = client.get("/incidence/consultar")
    assert response.status_code == 200
    assert "Consultar Incidencia" in response.text

def test_get_all_incidences():
    """Prueba que la ruta '/incidencias' devuelve correctamente todas las incidencias."""
    # Primero, crear algunas incidencias para probar
    uc = UniversalController()
    uc.add(IncidenceCreate(Descripcion="Incidencia1", Tipo="Tipo1", TicketID=5))
    uc.add(IncidenceCreate(Descripcion="Incidencia2", Tipo="Tipo2", TicketID=6))
    response = client.get("/incidence/incidencias")
    assert response.status_code == 200
    data: List[Dict[str, Any]] = response.json()  # Type the data
    assert len(data) >= 2
    assert data[0]["Descripcion"] in ["Incidencia1", "Incidencia2"]
    assert data[0]["Tipo"] in ["Tipo1", "Tipo2"]
    assert data[0]["TicketID"] in [5, 6]

def test_get_incidence_by_id_existing():
    """Prueba que la ruta '/incidencia/{IncidenciaID}' devuelve la incidencia correcta cuando existe."""
    # Primero, crear una incidencia para probar
    uc = UniversalController()
    created = uc.add(IncidenceCreate(Descripcion="FindByIDE", Tipo="TipoIDE", TicketID=7))
    incidence_id = created.IncidenciaID

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
    assert response.json()["detail"] == "Incidence not found"

def test_listar_incidencias():
    """Prueba la consulta de todas las incidencias."""
    controller = UniversalController()
    controller.add(Incidence(description="Accidente", status="Abierto", type="Choque"))
    response = client.get("/incidences/")
    assert response.status_code == 200
    assert "Accidente" in response.text

def test_detalle_incidencia_existente():
    """Prueba la consulta de una incidencia existente por ID."""
    controller = UniversalController()
    controller.add(Incidence(incidence_id=1, description="Accidente", status="Abierto", type="Choque"))
    response = client.get("/incidences/1")
    assert response.status_code == 200
    assert "Accidente" in response.text

def test_detalle_incidencia_no_existente():
    """Prueba la consulta de una incidencia inexistente."""
    response = client.get("/incidences/999")
    assert response.status_code == 404
    assert "Incidencia no encontrada" in response.text
