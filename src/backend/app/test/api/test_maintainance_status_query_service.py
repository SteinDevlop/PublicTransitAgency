from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_query_service import app as status_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.maintainance_status import MaintainanceStatusCreate, MaintainanceStatusOut # Importar el modelo de salida
from typing import List, Dict, Any

# Limpieza de base de datos antes y después de cada test
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(status_router)
client = TestClient(app_for_test)

def test_consultar_page():
    """Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarEstatusMantenimiento.html' correctamente."""
    response = client.get("/maintainance_status/consultar")
    assert response.status_code == 200
    assert "Consultar Estatus de Mantenimiento" in response.text

def test_get_all_status():
    """Prueba que la ruta '/status' devuelve correctamente todos los estados de mantenimiento."""
    # Primero, crear algunos estados de mantenimiento para probar
    uc = UniversalController()
    uc.add(MaintainanceStatusCreate(TipoEstado="Estado1", UnidadTransporte="Unidad-A", Status="Activo"))
    uc.add(MaintainanceStatusCreate(TipoEstado="Estado2", UnidadTransporte="Unidad-B", Status="Inactivo"))

    response = client.get("/maintainance_status/status")
    assert response.status_code == 200
    data: List[Dict[str, Any]] = response.json()  # Anotación de tipo
    assert len(data) >= 2  # Verifica que al menos se devuelvan los estados creados
    assert data[0]["TipoEstado"] in ["Estado1", "Estado2"]
    assert data[0]["Status"] in ["Activo", "Inactivo"]
    assert data[0]["UnidadTransporte"] in ["Unidad-A", "Unidad-B"] # Verificamos tambien la unidad de transporte

def test_get_status_by_id_existing():
    """Prueba que la ruta '/status/{ID}' devuelve el estado correcto cuando existe."""
    # Primero, crear un estado de mantenimiento para probar
    uc = UniversalController()
    created = uc.add(MaintainanceStatusCreate(TipoEstado="FindByIDE", UnidadTransporte="Unidad-C", Status="Activo"))
    status_id = created.ID

    response = client.get(f"/maintainance_status/status/{status_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["TipoEstado"] == "FindByIDE"
    assert data["UnidadTransporte"] == "Unidad-C"
    assert data["Status"] == "Activo"

def test_get_status_by_id_not_found():
    """Prueba que la ruta '/status/{ID}' devuelve un error 404 cuando no encuentra el estado."""
    response = client.get("/maintainance_status/status/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Maintainance Status not found"
