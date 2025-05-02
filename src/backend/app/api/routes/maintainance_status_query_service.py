from fastapi import FastAPI, Form, Request, HTTPException, APIRouter, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.maintainance_status import MaintainanceStatus
from backend.app.logic.universal_controller_sql import UniversalController
from fastapi.testclient import TestClient
from backend.app.api.routes.maintainance_status_query_service import app as maintainance_router
from typing import List, Dict, Any

app = APIRouter(prefix="/maintainance-status", tags=["maintainance-status"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_estados(request: Request):
    """Renders the 'ListarMaintainanceStatus.html' template with all maintainance statuses."""
    estados = controller.read_all(MaintainanceStatus(status=""))
    return templates.TemplateResponse("ListarMaintainanceStatus.html", {"request": request, "estados": estados})

@app.get("/{id}", response_class=HTMLResponse)
def detalle_estado(id: int, request: Request):
    """Renders the 'DetalleMaintainanceStatus.html' template for a specific maintainance status."""
    estado = controller.get_by_id(MaintainanceStatus, id)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado de mantenimiento no encontrado")
    return templates.TemplateResponse("DetalleMaintainanceStatus.html", {"request": request, "estado": estado})

# Limpieza de base de datos antes y después de cada test
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(maintainance_router)
client = TestClient(app_for_test)

def test_get_all_status():
    """Prueba que la ruta '/' devuelve correctamente todos los estados de mantenimiento."""
    # Primero, crear algunos estados de mantenimiento para probar
    uc = UniversalController()
    uc.add(MaintainanceStatus(status="No hecho"))
    uc.add(MaintainanceStatus(status="En progreso"))

    response = client.get("/maintainance-status/")
    assert response.status_code == 200
    assert "No hecho" in response.text
    assert "En progreso" in response.text

def test_get_status_by_id_existing():
    """Prueba que la ruta '/{id}' devuelve el estado correcto cuando existe."""
    # Primero, crear un estado de mantenimiento para probar
    uc = UniversalController()
    created = uc.add(MaintainanceStatus(status="Hecho"))
    status_id = created["id"]

    response = client.get(f"/maintainance-status/{status_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "Hecho"

def test_get_status_by_id_not_found():
    """Prueba que la ruta '/{id}' devuelve un error 404 cuando no encuentra el estado."""
    response = client.get("/maintainance-status/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Estado de mantenimiento no encontrado"
