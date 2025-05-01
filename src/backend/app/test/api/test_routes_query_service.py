from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.routes_query_service import app as routes_router
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.routes import RouteCreate, RouteOut
from typing import List, Dict, Any
import json

# Limpieza de base de datos antes y después de cada test
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(routes_router)
client = TestClient(app_for_test)

def test_list_routes_page():
    """Prueba que la ruta '/rutas' devuelve la plantilla 'ListarRutas.html' correctamente."""
    response = client.get("/routes/listar")  # Changed to /routes/listar
    assert response.status_code == 200
    assert "Listar Rutas" in response.text

def test_get_all_routes():
    """Prueba que la ruta '/all' devuelve correctamente todas las rutas."""  # Changed to /all
    # Primero, crear algunas rutas para probar
    uc = UniversalController()
    uc.add(RouteCreate(route_id="route1", route_name="Route 1", destination="Destination 1"))
    uc.add(RouteCreate(route_id="route2", route_name="Route 2", destination="Destination 2"))
    response = client.get("/routes/all")  # Changed to /routes/all
    assert response.status_code == 200
    data: List[Dict[str, Any]] = response.json()
    assert len(data) >= 2
    assert data[0]["route_name"] in ["Route 1", "Route 2"]
    assert data[0]["destination"] in ["Destination 1", "Destination 2"]
    assert data[0]["route_id"] in ["route1", "route2"]


def test_get_route_by_id_existing():
    """Prueba que la ruta '/{route_id}' devuelve la ruta correcta cuando existe.""" # Changed to /{route_id}
    # Primero, crear una ruta para probar
    uc = UniversalController()
    created = uc.add(RouteCreate(route_id="route_find", route_name="Route Find", destination="Destination Find"))
    route_id = created.route_id

    response = client.get(f"/routes/{route_id}")  # Changed to /routes/{route_id}
    assert response.status_code == 200
    data = response.json()
    assert data["route_name"] == "Route Find"
    assert data["destination"] == "Destination Find"
    assert data["route_id"] == "route_find"

def test_get_route_by_id_not_found():
    """Prueba que la ruta '/{route_id}' devuelve un error 404 cuando no encuentra la ruta.""" # Changed to /{route_id}
    response = client.get("/routes/nonexistent_route") # Changed to /routes/nonexistent_route
    assert response.status_code == 404
    assert response.json()["detail"] == "Route not found"

def test_route_detail_page_existing():
    """Prueba que la ruta '/detalles/{route_id}' devuelve la página de detalles correcta cuando existe la ruta.""" # Changed to /detalles/{route_id}
    uc = UniversalController()
    created = uc.add(RouteCreate(route_id="route_detail", route_name="Route Detail", destination="Destination Detail"))
    route_id = created.route_id

    response = client.get(f"/routes/detalles/{route_id}") # Changed to /routes/detalles/{route_id}
    assert response.status_code == 200
    assert "Detalle de Ruta" in response.text

def test_route_detail_page_not_found():
    """Prueba que la ruta '/detalles/{route_id}' devuelve un error 404 cuando no encuentra la ruta."""  # Changed to /detalles/{route_id}
    response = client.get("/routes/detalles/nonexistent_route")  # Changed to /routes/detalles/nonexistent_route
    assert response.status_code == 404
    assert response.json()["detail"] == "Route not found"
