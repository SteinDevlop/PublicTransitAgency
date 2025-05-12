import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_cud_service import app
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

def test_crear_ruta():
    """
    Prueba para crear una nueva ruta.
    """
    ruta = Route(ID=9998, IDHorario=2, Nombre="Nueva Ruta")
    try:
        response = client.post("/routes/create", data=ruta.to_dict(), headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Ruta creada exitosamente."
    finally:
        controller.delete(ruta)

def test_actualizar_ruta(setup_and_teardown):
    """
    Prueba para actualizar una ruta existente.
    """
    ruta = setup_and_teardown
    response = client.post(
        "/routes/update",
        data={"ID": ruta.ID, "IDHorario": 3, "Nombre": "Ruta Actualizada"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Ruta actualizada exitosamente."

def test_eliminar_ruta(setup_and_teardown):
    """
    Prueba para eliminar una ruta existente.
    """
    ruta = setup_and_teardown
    response = client.post("/routes/delete", data={"ID": ruta.ID}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Ruta eliminada exitosamente."