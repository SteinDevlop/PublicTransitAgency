import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_cud_service import app
from backend.app.models.incidence import Incidence
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.core.conf import headers

client = TestClient(app)
controller = UniversalController()

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    incidencia = Incidence(IDTicket=1, Descripcion="Prueba de incidencia", Tipo="Error", IDUnidad=1)
    controller.add(incidencia)
    created_incidencia = controller.read_all(Incidence)[-1]
    yield created_incidencia
    controller.delete(created_incidencia)

def test_crear_incidencia():
    """
    Prueba para crear una incidencia.
    """
    incidencia = Incidence(IDTicket=1, Descripcion="Nueva incidencia", Tipo="Advertencia", IDUnidad=1)
    try:
        response = client.post("/incidences/create", data=incidencia.to_dict(), headers=headers)
        assert response.status_code == 200
        assert response.json()["message"] == "Incidencia creada exitosamente."
    finally:
        created_incidencia = controller.read_all(Incidence)[-1]
        controller.delete(created_incidencia)

def test_actualizar_incidencia(setup_and_teardown):
    """
    Prueba para actualizar una incidencia existente.
    """
    incidencia = setup_and_teardown
    response = client.post(
        "/incidences/update",
        data={
            "ID": incidencia.ID,
            "IDTicket": 1,
            "Descripcion": "Incidencia actualizada",
            "Tipo": "Advertencia",
            "IDUnidad": 1
        },
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Incidencia actualizada exitosamente."

def test_eliminar_incidencia(setup_and_teardown):
    """
    Prueba para eliminar una incidencia existente.
    """
    incidencia = setup_and_teardown
    response = client.post("/incidences/delete", data={"ID": incidencia.ID}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Incidencia eliminada exitosamente."

