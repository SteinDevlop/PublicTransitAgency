from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app as incidence_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import IncidenceCreate

# Crear una instancia de FastAPI para pruebas
app_for_test = FastAPI()
app_for_test.include_router(incidence_router)
client = TestClient(app_for_test)

# Configuración del controlador para limpiar la base de datos antes de cada prueba
controller = UniversalController()

def setup_function():
    controller.clear_tables()

def teardown_function():
    controller.clear_tables()

def test_consultar_incidencias():
    """Prueba la consulta de todas las incidencias."""
    # Crear incidencias de prueba
    controller.add(IncidenceCreate(IncidenciaID=1, Descripcion="Falla técnica", Tipo="Técnica", TicketID=101))
    controller.add(IncidenceCreate(IncidenciaID=2, Descripcion="Falla operativa", Tipo="Operativa", TicketID=102))

    # Consultar todas las incidencias
    response = client.get("/incidence/consultar")
    assert response.status_code == 200
    assert "Falla técnica" in response.text
    assert "Falla operativa" in response.text

def test_obtener_incidencia_existente():
    """Prueba la obtención de una incidencia existente por su ID."""
    # Crear una incidencia de prueba
    controller.add(IncidenceCreate(IncidenciaID=1, Descripcion="Falla técnica", Tipo="Técnica", TicketID=101))

    # Consultar la incidencia por ID
    response = client.get("/incidence/incidencia/1")
    assert response.status_code == 200
    data = response.json()
    assert data["IncidenciaID"] == 1
    assert data["Descripcion"] == "Falla técnica"
    assert data["Tipo"] == "Técnica"
    assert data["TicketID"] == 101

def test_obtener_incidencia_no_existente():
    """Prueba la obtención de una incidencia inexistente por su ID."""
    # Consultar una incidencia que no existe
    response = client.get("/incidence/incidencia/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidence not found"