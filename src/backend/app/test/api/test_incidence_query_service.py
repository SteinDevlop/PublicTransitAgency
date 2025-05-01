"""from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app as incidences_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.incidence import Incidence

client = TestClient(incidences_router)

def setup_function():
    |||Limpia las tablas antes de cada prueba.|||
    UniversalController().clear_tables()

def teardown_function():
    |||Limpia las tablas después de cada prueba.|||
    UniversalController().clear_tables()

def test_listar_incidencias():
    |||Prueba que la ruta '/' devuelve correctamente todas las incidencias.|||
    controller = UniversalController()
    controller.add(Incidence(description="Accidente", status="Abierto", type="Choque"))
    controller.add(Incidence(description="Falla mecánica", status="Cerrado", type="Mecánico"))
    response = client.get("/incidences/")
    assert response.status_code == 200
    assert "Accidente" in response.text
    assert "Falla mecánica" in response.text

def test_detalle_incidencia_existente():
    |||Prueba que la ruta '/{incidence_id}' devuelve la incidencia correcta cuando existe.|||
    controller = UniversalController()
    controller.add(Incidence(incidence_id=1, description="Accidente", status="Abierto", type="Choque"))
    response = client.get("/incidences/1")
    assert response.status_code == 200
    assert "Accidente" in response.text
    assert "Abierto" in response.text
    assert "Choque" in response.text

def test_detalle_incidencia_no_existente():
    |||Prueba que la ruta '/{incidence_id}' devuelve un error 404 cuando no encuentra la incidencia.|||
    response = client.get("/incidences/999")
    assert response.status_code == 404
    assert "Incidencia no encontrada" in response.text
"""    