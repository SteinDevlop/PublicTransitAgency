import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from backend.app.api.routes.stops_query_service import app as paradas_router
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.models.stops import Parada
from backend.app.core.conf import headers

# Crear configuración de pruebas con FastAPI
app_for_test = FastAPI()
app_for_test.include_router(paradas_router)
client = TestClient(app_for_test)
controller = UniversalController()

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    Configuración y limpieza automática para cada prueba.
    """
    controller.clear_tables()
    yield
    controller.clear_tables()

def test_listar_paradas():
    """
    Test: Verificar que el endpoint /paradas/ devuelve todas las paradas registradas.
    """
    # Agregar paradas en la BD como datos de prueba
    controller.add(Parada(id=999, name="Parada 999", ubication="Ubicación 999"))
    controller.add(Parada(id=1000, name="Parada 1000", ubication="Ubicación 1000"))

    # Realizar solicitud al endpoint que lista las paradas
    response = client.get("/paradas/", headers=headers)

    # Verificar que la respuesta sea correcta
    assert response.status_code == 200
    assert "Parada 999" in response.text
    assert "Parada 1000" in response.text
    assert "Ubicación 999" in response.text
    assert "Ubicación 1000" in response.text

def test_detalle_parada_existente():
    """
    Test: Verificar que el endpoint /paradas/{id} devuelve los detalles de una parada existente.
    """
    # Agregar una parada en la BD como dato de prueba
    controller.add(Parada(id=999, name="Parada 999", ubication="Ubicación 999"))

    # Realizar solicitud al endpoint de detalles
    response = client.get("/paradas/999", headers=headers)

    # Verificar que la respuesta sea correcta
    assert response.status_code == 200
    assert "Parada 999" in response.text
    assert "Ubicación 999" in response.text

def test_detalle_parada_no_existente():
    """
    Test: Verificar que el endpoint /paradas/{id} maneja correctamente el caso de una parada inexistente.
    """
    # Realizar solicitud al endpoint con un ID inexistente
    response = client.get("/paradas/998", headers=headers)

    # Verificar que la respuesta sea un error 404 con el mensaje adecuado
    assert response.status_code == 404
    assert response.json()["detail"] == "Parada no encontrada"