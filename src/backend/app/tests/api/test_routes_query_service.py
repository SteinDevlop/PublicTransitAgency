import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_query_service import app
from backend.app.models.routes import Route
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers

client = TestClient(app)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    ruta = Route(ID=9999, IDHorario=1, Nombre="Ruta de Prueba")
    controller.add(ruta)
    yield ruta
    controller.delete(ruta)

def test_listar_rutas(setup_and_teardown):
    """
    Prueba para listar todas las rutas.
    """
    response = client.get("/routes/", headers=headers)
    assert response.status_code == 200

def test_detalle_ruta_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de una ruta existente.
    """
    ruta = setup_and_teardown
    response = client.get(f"/routes/{ruta.ID}", headers=headers)
    assert response.status_code == 200
    assert "Ruta de prueba" in response.text



