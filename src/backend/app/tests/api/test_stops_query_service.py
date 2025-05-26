import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_query_service import app
from backend.app.models.stops import Parada
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.core.conf import headers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.stops_query_service")

client = TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def setup_and_teardown():
    parada = Parada(ID=999999, Nombre="Parada de Prueba", Ubicacion="Ubicación de Prueba")
    existing_parada = controller.get_by_id(Parada, parada.ID)
    if existing_parada:
        controller.delete(existing_parada)
    controller.add(parada)
    yield parada
    controller.delete(parada)

def test_listar_paradas(setup_and_teardown):
    response = client.get("/stops/", headers=headers)
    assert response.status_code == 200
    assert "Parada de Prueba" in response.text
    logger.info("Test listar_paradas ejecutado correctamente.")

def test_detalle_parada_existente(setup_and_teardown):
    parada = setup_and_teardown
    response = client.get(f"/stops/{parada.ID}", headers=headers)
    assert response.status_code == 200
    assert str(parada.ID) in response.text
    assert "Parada de Prueba" in response.text
    logger.info(f"Test detalle_parada_existente ejecutado correctamente para ID={parada.ID}.")

def test_detalle_parada_no_existente():
    response = client.get("/stops/88888", headers=headers)
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test detalle_parada_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )