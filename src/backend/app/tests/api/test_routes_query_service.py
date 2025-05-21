import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_query_service import app
from backend.app.models.routes import Route
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.core.conf import headers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.routes_query_service")

client = TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def setup_and_teardown():
    ruta = Route(ID=9999, IDHorario=1, Nombre="Ruta de Prueba")
    controller.add(ruta)
    yield ruta
    controller.delete(ruta)

def test_listar_rutas(setup_and_teardown):
    response = client.get("/routes/", headers=headers)
    assert response.status_code == 200
    logger.info("Test listar_rutas ejecutado correctamente.")

def test_detalle_ruta_existente(setup_and_teardown):
    ruta = setup_and_teardown
    response = client.get(f"/routes/{ruta.ID}", headers=headers)
    assert response.status_code == 200
    assert str(ruta.ID) in response.text
    assert "Ruta de Prueba" in response.text
    logger.info(f"Test detalle_ruta_existente ejecutado correctamente para ID={ruta.ID}.")

def test_detalle_ruta_no_existente():
    response = client.get("/routes/99999", headers=headers)
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test detalle_ruta_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )