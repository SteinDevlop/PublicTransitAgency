# import pytest
# from fastapi.testclient import TestClient
# from backend.app.api.routes.transport_unit_query_service import app
# from backend.app.models.transport import Transport
# from backend.app.logic.universal_controller_sqlserver import UniversalController
# from backend.app.core.conf import headers

# client = TestClient(app)
# controller = UniversalController()

# @pytest.fixture
# def setup_and_teardown():
#     """
#     Fixture para configurar y limpiar los datos de prueba.
#     Crea una unidad de transporte antes de cada test y la elimina después.
#     """
#     transport = Transport(Ubicacion="Estación Central", Capacidad=50, IDRuta=1, IDTipo=2)
#     # Crear la unidad de prueba
#     controller.add(transport)
#     created_transport = controller.read_all(Transport)[-1]  # Obtener el último registro creado
#     yield created_transport

#     # Eliminar la unidad de prueba
#     controller.delete(created_transport)

# def test_listar_unidades(setup_and_teardown):
#     """
#     Prueba para listar todas las unidades de transporte.
#     Verifica que el endpoint /transports/ devuelve un código de estado 200
#     y que la unidad de transporte de prueba aparece en la respuesta.
#     """
#     response = client.get("/transports/", headers=headers)
#     assert response.status_code == 200
#     assert "Estación Central" in response.text

# def test_detalle_unidad_existente(setup_and_teardown):
#     """
#     Prueba para obtener el detalle de una unidad de transporte existente.
#     Verifica que el endpoint /transports/{ID} devuelve un código de estado 200
#     y que los detalles de la unidad de transporte de prueba aparecen en la respuesta.
#     """
#     transport = setup_and_teardown
#     response = client.get(f"/transports/{transport.ID}", headers=headers)
#     assert response.status_code == 200
#     assert "Estación Central" in response.text

# def test_detalle_unidad_no_existente():
#     """
#     Prueba para obtener el detalle de una unidad de transporte que no existe.
#     Verifica que el endpoint /transports/{ID} devuelve un código de estado 404
#     cuando se consulta una unidad de transporte inexistente.
#     """
#     response = client.get("/transports/99999", headers=headers)
#     assert response.status_code == 404
#     assert response.json()["detail"] == "Unidad de transporte no encontrada"