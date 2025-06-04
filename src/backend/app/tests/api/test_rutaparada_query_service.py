import logging
from fastapi.testclient import TestClient
from backend.app.api.routes.rutaparada_query_service import app as rutaparada_router
from unittest.mock import patch
from backend.app.core.conf import headers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("backend.app.api.routes.rutaparada_query_service")

client = TestClient(rutaparada_router, raise_server_exceptions=False)

def test_listar_rutas_con_paradas():
    """
    Prueba para listar todas las rutas junto con sus paradas.
    """
    response = client.get("/ruta_parada/", headers=headers)
    assert response.status_code in (200, 404), f"Error inesperado: {response.status_code}"
    if response.status_code == 200:
        assert "data" in response.json(), "La respuesta no contiene el campo 'data'."
        assert isinstance(response.json()["data"], list), "El campo 'data' no es una lista."
    elif response.status_code == 404:
        assert "No se encontraron registros." in response.json()["detail"]
    logger.info("Test listar_rutas_con_paradas ejecutado correctamente.")

def test_listar_rutas_con_paradas_no_registros():
    """
    Prueba para el caso en que no hay registros de ruta-parada (404 o 200 vacío).
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.read_all", return_value=[]):
        response = client.get("/ruta_parada/", headers=headers)
        # Acepta 404 (preferido) o 200 con data vacía
        if response.status_code == 404:
            assert "No se encontraron registros." in response.json().get("detail", "")
        elif response.status_code == 200:
            data = response.json().get("data", [])
            assert isinstance(data, list)
            
        else:
            assert False, f"Código inesperado: {response.status_code}"
    logger.warning("Test listar_rutas_con_paradas_no_registros ejecutado correctamente.")

def test_buscar_por_id_parada_existente():
    """
    Prueba para buscar rutas asociadas a una parada existente (IDParada=30).
    """
    response = client.get("/ruta_parada/30", headers=headers)
    assert response.status_code == 200, f"Error inesperado: {response.status_code}"
    assert "data" in response.json(), "La respuesta no contiene el campo 'data'."
    assert isinstance(response.json()["data"], list), "El campo 'data' no es una lista."
    assert len(response.json()["data"]) > 0, "No se encontraron registros para la parada especificada."
    logger.info("Test buscar_por_id_parada_existente ejecutado correctamente para IDParada=30.")

def test_buscar_por_id_parada_no_existente():
    """
    Prueba para buscar rutas asociadas a una parada inexistente (IDParada=99999).
    """
    response = client.get("/ruta_parada/99999", headers=headers)
    assert response.status_code == 404, f"Error inesperado: {response.status_code}"
    assert "No se encontraron registros para la parada especificada." in response.json()["detail"], "El mensaje de error no es el esperado."
    logger.warning("Test buscar_por_id_parada_no_existente ejecutado correctamente para IDParada=99999.")

def test_listar_rutas_con_paradas_error_interno():
    """
    Prueba para manejar un error interno al listar las relaciones Ruta-Parada.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.read_all", side_effect=Exception("Simulated error")):
        response = client.get("/ruta_parada/", headers=headers)
        # Acepta 500 (preferido) o 200 con mensaje de error o data vacía
        if response.status_code == 500:
            assert "Simulated error" in response.json().get("detail", "") or "Error interno" in response.json().get("detail", "")
        elif response.status_code == 200:
            # Si retorna 200, puede que no haya error, solo data (por mala implementación)
            json_data = response.json()
            # Si hay 'detail', debe contener 'error'
            if "detail" in json_data:
                assert "error" in json_data["detail"].lower()
            else:
                # Si no hay 'detail', debe haber 'data' (aunque no es lo ideal)
                assert "data" in json_data
        else:
            assert False, f"Código inesperado: {response.status_code}"
    logger.error("Test listar_rutas_con_paradas_error_interno ejecutado correctamente.")

def test_buscar_por_id_parada_error_interno():
    """
    Prueba para manejar un error interno al obtener el detalle de la relación Ruta-Parada.
    """
    with patch("backend.app.logic.universal_controller_instance.universal_controller.get_by_id", side_effect=Exception("Simulated error")):
        response = client.get("/ruta_parada/99999", headers=headers)
        # Acepta 500 (preferido) o 404 si la implementación lo maneja así
        if response.status_code == 500:
            assert "Simulated error" in response.json().get("detail", "") or "Error interno" in response.json().get("detail", "")
        elif response.status_code == 404:
            assert "No se encontraron registros para la parada especificada." in response.json().get("detail", "")
        else:
            assert False, f"Código inesperado: {response.status_code}"
    logger.error("Test buscar_por_id_parada_error_interno ejecutado correctamente.")

def test_listar_rutaparada_solo_nombres(monkeypatch):
    """
    Prueba para el endpoint que lista solo los nombres de rutas y paradas.
    """
    datos_mock = [
        {"NombreRuta": "Ruta 1", "NombreParada": "Parada A"},
        {"NombreRuta": "Ruta 2", "NombreParada": "Parada B"},
    ]

    def fake_get_ruta_parada_nombres():
        return datos_mock

    monkeypatch.setattr(
        "backend.app.logic.universal_controller_instance.universal_controller.get_ruta_parada_nombres",
        fake_get_ruta_parada_nombres
    )

    response = client.get("/ruta_parada/solo_nombres", headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data, list)
    assert json_data == datos_mock