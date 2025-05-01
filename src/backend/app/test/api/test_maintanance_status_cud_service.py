from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_query_service import app as status_router
from backend.app.models.maintainance_status import MaintainanceStatusOut # Importa el modelo

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
    client.post(
        "/maintainance_status/create",
        data={"TipoEstado": "Estado1", "UnidadTransporte": "Unidad-A", "Status": "Activo"}
    )
    client.post(
        "/maintainance_status/create",
        data={"TipoEstado": "Estado2", "UnidadTransporte": "Unidad-B", "Status": "Inactivo"}
    )
    response = client.get("/maintainance_status/status")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # Verifica que al menos se devuelvan los estados creados
    assert data[0]["TipoEstado"] in ["Estado1", "Estado2"]
    assert data[0]["Status"] in ["Activo", "Inactivo"]

def test_get_status_by_id_existing():
    """Prueba que la ruta '/status/{ID}' devuelve el estado correcto cuando existe."""
    # Primero, crear un estado de mantenimiento para probar
    create_response = client.post(
        "/maintainance_status/create",
        data={"TipoEstado": "FindByIDE", "UnidadTransporte": "Unidad-C", "Status": "Activo"}
    )
    assert create_response.status_code == 200
    created_data = create_response.json()["data"]
    status_id = created_data["ID"]

    response = client.get(f"/maintainance_status/status/{status_id}")
    assert response.status_code == 200 # El código de estado debe ser 200 para una respuesta exitosa
    data = response.json() # Parsea la respuesta JSON para obtener los datos
    # Verifica que los datos coincidan con lo que se creó
    assert data["TipoEstado"] == "FindByIDE"
    assert data["UnidadTransporte"] == "Unidad-C"
    assert data["Status"] == "Activo"

def test_get_status_by_id_not_found():
    """Prueba que la ruta '/status/{ID}' devuelve un error 404 cuando no encuentra el estado."""
    response = client.get("/maintainance_status/status/9999")
    assert response.status_code == 404 # Debe retornar un 404 si no lo encuentra
    assert response.json()["detail"] == "Maintainance status not found"
