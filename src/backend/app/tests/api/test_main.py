import pytest
from fastapi.testclient import TestClient
from backend.app.api.main import app

def test_root_status():
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()

def test_static_files_served():
    client = TestClient(app)
    response = client.get("/static/")
    # Puede ser 200 o 404 si no hay archivos, pero no debe ser 500
    assert response.status_code in (200, 404)

def test_startup_and_shutdown_events():
    # No se puede probar directamente los eventos, pero se puede instanciar el cliente
    client = TestClient(app)
    # Si la app arranca y responde, los eventos se ejecutan
    response = client.get("/openapi.json")
    assert response.status_code == 200

@pytest.mark.parametrize("route", [
    "/reporte/supervisor",
    "/planificador/ubicaciones",
    "/login/token",
    "/maintainance/listar",
    "/user/consultar",
    "/price/consultar",
])
def test_included_routes(route):
    client = TestClient(app)
    # GET para la mayoría, POST para planificador/ubicaciones y login/token
    if route in ["/planificador/ubicaciones", "/login/token"]:
        response = client.post(route)
        # Puede ser 200, 400, 401, 422 según la ruta y datos
        assert response.status_code in (200, 400, 401, 422)
    else:
        response = client.get(route)
        assert response.status_code in (200, 401, 404)
