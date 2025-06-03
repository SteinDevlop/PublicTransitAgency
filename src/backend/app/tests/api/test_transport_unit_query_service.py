import pytest
import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.transport_unit_query_service import app
from backend.app.models.transport import UnidadTransporte
from backend.app.logic.universal_controller_instance import universal_controller as controller
from unittest.mock import patch

from backend.app.core.conf import headers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.transport_unit_query_service")

client = TestClient(app, raise_server_exceptions=False)

@pytest.fixture
def setup_and_teardown():
    """
    Fixture para configurar y limpiar los datos de prueba.
    """
    unidad = UnidadTransporte(Ubicacion="Depósito Central", Capacidad=50, IDRuta=1, IDTipo=2, ID="EMPTY")
    controller.add(unidad)
    yield unidad
    controller.delete(unidad)

def test_listar_unidades_transporte(setup_and_teardown):
    """
    Prueba para listar todas las unidades de transporte.
    """
    response = client.get("/transport_units/", headers=headers)
    assert response.status_code == 200
    response_json = response.json()
    assert isinstance(response_json, list), "La respuesta debe ser una lista"
    assert any(u["Ubicacion"] == "Depósito Central" for u in response_json)
    logger.info("Test listar_unidades_transporte ejecutado correctamente.")

def test_listar_unidades_transporte_formato_json(setup_and_teardown):
    """
    Prueba para listar todas las unidades de transporte en formato JSON.
    """
    response = client.get("/transport_units/", headers=headers)
    assert response.status_code == 200, f"Error inesperado: {response.status_code}"
    response_json = response.json()
    assert isinstance(response_json, list), "La respuesta debe ser una lista de unidades de transporte."
    assert len(response_json) > 0, "La lista de unidades de transporte está vacía."
    logger.info("Test listar_unidades_transporte_formato_json ejecutado correctamente.")

def test_detalle_unidad_transporte_existente(setup_and_teardown):
    """
    Prueba para obtener el detalle de una unidad de transporte existente.
    """
    unidad = setup_and_teardown
    response = client.get(f"/transport_units/{unidad.ID}", headers=headers)
    assert response.status_code == 200, f"Error inesperado: {response.status_code}"
    response_json = response.json()
    assert "data" in response_json, "La respuesta no contiene la clave 'data'."
    assert response_json["data"]["Ubicacion"] == "Depósito Central"
    logger.info(f"Test detalle_unidad_transporte_existente ejecutado correctamente para ID={unidad.ID}.")

def test_detalle_unidad_transporte_existente_formato_dict(setup_and_teardown):
    """
    Prueba para obtener el detalle de una unidad de transporte existente en formato dict.
    """
    unidad = setup_and_teardown
    response = client.get(f"/transport_units/{unidad.ID}", headers=headers)
    assert response.status_code == 200, f"Error inesperado: {response.status_code}"
    response_json = response.json()
    assert "data" in response_json, "La respuesta no contiene la clave 'data'."
    assert isinstance(response_json["data"], dict), "La respuesta no está en formato dict."
    logger.info(f"Test detalle_unidad_transporte_existente_formato_dict ejecutado correctamente para ID={unidad.ID}.")

def test_detalle_unidad_transporte_no_existente():
    """
    Prueba para manejar el caso en el que una unidad de transporte no existe.
    """
    response = client.get("/transport_units/NO_EXISTE", headers=headers)
    assert response.status_code == 404, f"Error inesperado: {response.status_code}"
    response_json = response.json()
    assert "detail" in response_json, "La respuesta no contiene la clave 'detail'."
    assert "No se encontró la unidad de transporte especificada." in response_json["detail"], "El mensaje de error no es el esperado."
    logger.warning("Test detalle_unidad_transporte_no_existente ejecutado correctamente.")

def test_detalle_unidad_transporte_error_interno():
    """
    Prueba para manejar un error interno al consultar una unidad de transporte.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_id", side_effect=Exception("Simulated error")):
        response = client.get("/transport_units/ERROR", headers=headers)
        assert response.status_code == 500, f"Error inesperado: {response.status_code}"
        response_json = response.json()
        assert "detail" in response_json, "La respuesta no contiene la clave 'detail'."
        assert "Error interno al consultar detalle de unidad de transporte." in response_json["detail"], "El mensaje de error no es el esperado."
        logger.error("Test detalle_unidad_transporte_error_interno ejecutado correctamente.")
def test_listar_unidades_con_horarios(setup_and_teardown):
    """
    Prueba para listar todas las unidades de transporte con sus horarios.
    """
    response = client.get("/transport_units/with_schedules", headers=headers)
    assert response.status_code == 200
    unidades = response.json()
    assert isinstance(unidades, list), "La respuesta debe ser una lista"
    assert any("horarios" in u for u in unidades), "Cada unidad debe tener la clave 'horarios'"
    # Si hay unidades con IDRuta, debe haber una lista (puede estar vacía)
    for u in unidades:
        assert "horarios" in u
        assert isinstance(u["horarios"], list)
    logger.info("Test listar_unidades_con_horarios ejecutado correctamente.")

def test_listar_unidades_con_nombres(setup_and_teardown):
    """
    Prueba para listar todas las unidades de transporte mostrando los nombres de ruta y tipo de transporte.
    """
    response = client.get("/transport_units/with_names", headers=headers)
    assert response.status_code == 200
    unidades = response.json()
    assert isinstance(unidades, list), "La respuesta debe ser una lista"
    for u in unidades:
        assert "ID" in u
        assert "Ubicacion" in u
        assert "Capacidad" in u
        assert "NombreRuta" in u
        assert "NombreTipoTransporte" in u
        assert "IDRuta" not in u
        assert "IDTipo" not in u
    logger.info("Test listar_unidades_con_nombres ejecutado correctamente.")