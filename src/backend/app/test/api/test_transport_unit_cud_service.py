# import pytest
# from fastapi.testclient import TestClient
# from backend.app.api.routes.transport_unit_cud_service import app
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
#     controller.add(transport)  # Agregamos la unidad a la base de datos
#     created_transport = controller.read_all(Transport)[-1]  # Obtenemos el último registro creado
#     yield created_transport  # Pasamos la unidad creada al test

#     # Eliminamos la unidad de transporte después de que el test se ejecuta
#     controller.delete(created_transport)

# def test_crear_unidad():
#     """
#     Prueba para crear una unidad de transporte.
#     Verifica que el endpoint /transports/create devuelve un código de estado 200
#     y que la unidad de transporte se crea correctamente.
#     """
#     transport = Transport(Ubicacion="Estación Norte", Capacidad=40, IDRuta=1, IDTipo=2)
#     try:
#         response = client.post("/transports/create", data=transport.to_dict(), headers=headers)
#         assert response.status_code == 200
#         assert response.json()["message"] == "Unidad de transporte creada exitosamente."
#     finally:
#         created_transport = controller.read_all(Transport)[-1]  # Obtenemos el último registro creado
#         controller.delete(created_transport)

# def test_actualizar_unidad(setup_and_teardown):
#     """
#     Prueba para actualizar una unidad de transporte existente.
#     Verifica que el endpoint /transports/update devuelve un código de estado 200
#     y que los datos de la unidad de transporte se actualizan correctamente.
#     """
#     transport = setup_and_teardown
#     response = client.post(
#         "/transports/update",
#         data={
#             "ID": transport.ID,
#             "Ubicacion": "Estación Sur",
#             "Capacidad": 60,
#             "IDRuta": 2,
#             "IDTipo": 3
#         },
#         headers=headers
#     )
#     assert response.status_code == 200
#     assert response.json()["message"] == "Unidad de transporte actualizada exitosamente."

#     updated_transport = controller.get_by_id(Transport, transport.ID)
#     assert updated_transport.Ubicacion == "Estación Sur"
#     assert updated_transport.Capacidad == 60

# def test_eliminar_unidad(setup_and_teardown):
#     """
#     Prueba para eliminar una unidad de transporte existente.
#     Verifica que el endpoint /transports/delete devuelve un código de estado 200
#     y que la unidad de transporte se elimina correctamente.
#     """
#     transport = setup_and_teardown
#     response = client.post("/transports/delete", data={"ID": transport.ID}, headers=headers)
#     assert response.status_code == 200
#     assert response.json()["message"] == "Unidad de transporte eliminada exitosamente."

#     deleted_transport = controller.get_by_id(Transport, transport.ID)
#     assert deleted_transport is None