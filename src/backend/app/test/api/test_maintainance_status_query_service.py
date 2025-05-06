import pytest
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_query_service import app
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.core.conf import headers

client = TestClient(app)
controller = UniversalController()

@pytest.fixture(autouse=True)
def limpiar_bd():
    # Limpia la base de datos antes y después de cada prueba
    controller.clear_tables()
    yield
    controller.clear_tables()

def test_listar_estados():
    # Agregamos datos de prueba
    controller.add(MaintainanceStatus(id=1, type="Preventivo", status="Activo"))
    controller.add(MaintainanceStatus(id=2, type="Correctivo", status="Inactivo"))

    # Enviamos una solicitud para listar los estados
    response = client.get("/maintainance_status/", headers=headers)

    # Comprobamos que la respuesta sea exitosa
    assert response.status_code == 200
    assert "Preventivo" in response.text
    assert "Activo" in response.text
    assert "Correctivo" in response.text
    assert "Inactivo" in response.text

def test_detalle_estado_existente():
    # Agregamos un estado de prueba
    controller.add(MaintainanceStatus(id=1, type="Preventivo", status="Activo"))
    # Enviamos una solicitud para obtener el detalle del estado
    response = client.get("/maintainance_status/1", headers=headers)
    # Comprobamos que la respuesta sea exitosa y que contenga los valores esperados
    assert response.status_code == 200
    assert "Preventivo" in response.text
    assert "Activo" in response.text

"""def test_detalle_estado_no_existente():
    # Intentamos acceder a un estado que no existe
    response = client.get("/maintainance_status/999", headers=headers)
    # Comprobamos que devuelva un error 404 con el mensaje correspondiente
    assert response.status_code == 404
    assert response.json()["detail"] == "Estado de mantenimiento no encontrado"
"""