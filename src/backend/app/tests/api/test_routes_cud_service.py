import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_cud_service import app
from backend.app.models.routes import Route
from backend.app.logic.universal_controller_instance import universal_controller as controller

from backend.app.core.conf import headers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.routes_cud_service")

client = TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def setup_and_teardown():
    ruta = Route(ID=9999, IDHorario=1, Nombre="Ruta de Prueba")
    controller.add(ruta)
    yield ruta
    controller.delete(ruta)

def test_crear_ruta():
    ruta = Route(ID=9998, IDHorario=2, Nombre="Nueva Ruta")
    try:
        response = client.post("/routes/create", data=ruta.to_dict(), headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Ruta creada exitosamente."
        logger.info("Test crear_ruta ejecutado correctamente.")
    finally:
        controller.delete(ruta)

def test_actualizar_ruta(setup_and_teardown):
    ruta = setup_and_teardown
    response = client.post(
        "/routes/update",
        data={"ID": ruta.ID, "IDHorario": 3, "Nombre": "Ruta Actualizada"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Ruta actualizada exitosamente."
    logger.info(f"Test actualizar_ruta ejecutado correctamente para ID={ruta.ID}.")

def test_actualizar_ruta_no_existente():
    response = client.post(
        "/routes/update",
        data={"ID": 99999, "IDHorario": 3, "Nombre": "No existe"},
        headers=headers
    )
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test actualizar_ruta_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )

def test_eliminar_ruta(setup_and_teardown):
    ruta = setup_and_teardown
    response = client.post("/routes/delete", data={"ID": ruta.ID}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Ruta eliminada exitosamente."
    logger.info(f"Test eliminar_ruta ejecutado correctamente para ID={ruta.ID}.")

def test_eliminar_ruta_no_existente():
    response = client.post("/routes/delete", data={"ID": 99999}, headers=headers)
    assert response.status_code in (404, 500)
    logger.warning(
        f"Test eliminar_ruta_no_existente ejecutado: status={response.status_code}, body={response.text}"
    )