"""from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_query_service import app as routes_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.routes import RouteCreate

def setup_function():
    uc = UniversalController()
    uc.clear_tables()
    # Crear algunas rutas de prueba
    uc.add(RouteCreate(route_id="RUT101", name="Ruta A", origin="Origen A", destination="Destino A"))
    uc.add(RouteCreate(route_id="RUT102", name="Ruta B", origin="Origen B", destination="Destino B"))

def teardown_function():
    UniversalController().clear_tables()

app_for_test = FastAPI()
app_for_test.include_router(routes_router)
client = TestClient(app_for_test)

def test_get_all_routes():
    response = client.get("/routes/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["route_id"] == "RUT101"
    assert data[0]["name"] == "Ruta A"
    assert data[1]["origin"] == "Origen B"

def test_get_route_by_id_existing():
    response = client.get("/routes/RUT101")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ruta A"
    assert data["destination"] == "Destino A"

def test_get_route_by_id_not_found():
    response = client.get("/routes/RUT999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Route not found"

def test_list_routes_page():
    response = client.get("/routes/listar")
    assert response.status_code == 200
    assert "Listado de Rutas" in response.text # Verifica el título de la página

def test_route_detail_page_existing():
    response = client.get("/routes/detalles/RUT102")
    assert response.status_code == 200
    assert "Detalle de la Ruta" in response.text # Verifica el título de la página
    assert "Ruta B" in response.text
    assert "Destino B" in response.text

def test_route_detail_page_not_found():
    response = client.get("/routes/detalles/RUT999")
    assert response.status_code == 200 # Aunque no encuentre, la página podría renderizar sin datos
    assert "Detalle de la Ruta" in response.text
    assert "None" in response.text # O algún indicador de que no se encontró

    """