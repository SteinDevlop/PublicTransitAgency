import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.stops_cud_service import app
from backend.app.models.stops import Parada
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.core.conf import headers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.stops_cud_service")

client = TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def setup_and_teardown():
    parada_prueba = Parada(ID=9999, Nombre="Parada de prueba", Ubicacion="Ubicación de prueba")
    existing_parada = controller.get_by_id(Parada, parada_prueba.ID)
    if existing_parada:
        controller.delete(existing_parada)
    controller.add(parada_prueba)
    yield parada_prueba
    controller.delete(parada_prueba)

def test_crear_parada():
    parada_prueba = Parada(ID=9998, Nombre="Nueva Parada", Ubicacion="Ubicación Nueva")
    try:
        response = client.post(
            "/stops/create",
            data={"id": parada_prueba.ID, "Nombre": parada_prueba.Nombre, "Ubicacion": parada_prueba.Ubicacion},
            headers=headers
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Parada creada exitosamente."
        logger.info("Test crear_parada ejecutado correctamente.")
    finally:
        controller.delete(parada_prueba)

def test_actualizar_parada(setup_and_teardown):
    parada_prueba = setup_and_teardown
    response = client.post(
        "/stops/update",
        data={"id": parada_prueba.ID, "Nombre": "Parada Actualizada", "Ubicacion": "Ubicación Actualizada"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Parada actualizada exitosamente."
    parada_actualizada = controller.get_by_id(Parada, parada_prueba.ID)
    assert parada_actualizada.Nombre == "Parada Actualizada"
    assert parada_actualizada.Ubicacion == "Ubicación Actualizada"
    logger.info(f"Test actualizar_parada ejecutado correctamente para ID={parada_prueba.ID}.")

def test_actualizar_parada_no_existente():
    response = client.post(
        "/stops/update",
        data={"id": 88888, "Nombre": "No existe", "Ubicacion": "No existe"},
        headers=headers
    )
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test actualizar_parada_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )

def test_eliminar_parada(setup_and_teardown):
    parada_prueba = setup_and_teardown
    response = client.post(
        "/stops/delete",
        data={"id": parada_prueba.ID},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Parada eliminada exitosamente."
    parada_eliminada = controller.get_by_id(Parada, parada_prueba.ID)
    assert parada_eliminada is None
    logger.info(f"Test eliminar_parada ejecutado correctamente para ID={parada_prueba.ID}.")

def test_eliminar_parada_no_existente():
    response = client.post(
        "/stops/delete",
        data={"id": 88888},
        headers=headers
    )
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test eliminar_parada_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )