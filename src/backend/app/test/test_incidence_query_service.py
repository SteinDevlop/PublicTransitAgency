from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException, Request, Query, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import pytest
from unittest.mock import MagicMock

#from backend.app.models.incidence import IncidenceOut
from logic.universal_controller_sql import UniversalController

# Para simplificar, definimos modelos y controlador mock aquí
class IncidenceOut:
    def __init__(self, incidence_id: int, description: str, type: str, status: str):
        self.incidence_id = incidence_id
        self.description = description
        self.type = type
        self.status = status

    def dict(self):
        return {"incidence_id": self.incidence_id, "description": self.description, "type": self.type, "status": self.status}
    
    @staticmethod
    def get_empty_instance():
        return IncidenceOut(incidence_id=None, description=None, type=None, status=None)


class MockController:
    def __init__(self):
        self.data = {
            1: IncidenceOut(incidence_id=1, description="Descripción 1", type="Tipo 1", status="Pendiente"),
            2: IncidenceOut(incidence_id=2, description="Descripción 2", type="Tipo 2", status="Resuelto"),
            3: IncidenceOut(incidence_id=3, description="Descripción 3", type="Tipo 3", status="Pendiente"),
            4: IncidenceOut(incidence_id=4, description="Descripción 4", type="Tipo 4", status="En Progreso"),
            5: IncidenceOut(incidence_id=5, description="Descripción 5", type="Tipo 5", status="Resuelto"),
        }

    def read_all(self, model):
        return list(self.data.values())

    def get_by_id(self, model, incidence_id):
        return self.data.get(incidence_id)

app_for_test = FastAPI()

mock_controller = MockController()
mock_templates = MagicMock()

# Incluir el router con el controlador mock
app = APIRouter(prefix="/incidences", tags=["incidencias"])

@app.get("", response_class=HTMLResponse)
async def listar_incidencias_html(
    request: Request,
    skip: int = Query(0, description="Registros a saltar"),
    limit: int = Query(10, description="Límite de resultados"),
    status: str = Query(None, description="Filtrar por estado (opcional)")
):
    try:
        dummy = IncidenceOut.get_empty_instance()
        all_data = mock_controller.read_all(dummy)

        # Filtrado por estado (si se especifica)
        if status:
            filtered_data = [item for item in all_data if item.status == status]
        else:
            filtered_data = all_data

        # Paginación
        paginated_data = filtered_data[skip:skip + limit]
        return mock_templates.TemplateResponse("ListarIncidencia.html", {"request": request, "incidencias": paginated_data})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint 1 (JSON): Obtener todas las incidencias (con paginación y filtro) - JSON
@app.get("/json")
async def listar_incidencias_json(
    skip: int = Query(0, description="Registros a saltar"),
    limit: int = Query(10, description="Límite de resultados"),
    status: str = Query(None, description="Filtrar por estado (opcional)")
):
    try:
        dummy = IncidenceOut.get_empty_instance()
        all_data = mock_controller.read_all(dummy)

        # Filtrado por estado (si se especifica)
        if status:
            filtered_data = [item for item in all_data if item.status == status]
        else:
            filtered_data = all_data

        # Paginación
        paginated_data = filtered_data[skip:skip + limit]
        return JSONResponse(content={"data": [item.dict() for item in paginated_data]})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint 2: Obtener incidencia por ID - HTML
@app.get("/{incidence_id}", response_class=HTMLResponse)
async def obtener_incidencia_html(request: Request, incidence_id: int = Query(...)):
    try:
        incidence = mock_controller.get_by_id(IncidenceOut, incidence_id)
        if not incidence:
            raise HTTPException(status_code=404, detail="Incidencia no encontrada")
        return mock_templates.TemplateResponse("DetalleIncidencia.html", {"request": request, "incidencia": incidence})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint 2 (JSON): Obtener incidencia por ID - JSON
@app.get("/{incidence_id}/json")
async def obtener_incidencia_json(incidence_id: int = Query(...)):
    try:
        incidence = mock_controller.get_by_id(IncidenceOut, incidence_id)
        if not incidence:
            raise HTTPException(status_code=404, detail="Incidencia no encontrada")
        return JSONResponse(content={"data": incidence.dict()})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint para la página de consulta principal (HTML)
@app.get("/consultar", response_class=HTMLResponse)
def consultar_incidencias(request: Request):
    return mock_templates.TemplateResponse("ConsultarIncidencia", {"request": request})

app_for_test.include_router(app) #incluimos el router

# Cliente de prueba
client = TestClient(app_for_test)

# Tests para /incidences (HTML)
def test_listar_incidencias_html():
    response = client.get("/incidences")
    assert response.status_code == 200
    mock_templates.TemplateResponse.assert_called_once_with(
        "ListarIncidencia.html", {"request": MagicMock(), "incidencias": list(MockController().data.values())[:10]}
    )

def test_listar_incidencias_html_pagination():
    response = client.get("/incidences?skip=2&limit=2")
    assert response.status_code == 200
    expected_data = list(MockController().data.values())[2:4]
    mock_templates.TemplateResponse.assert_called_once_with(
        "ListarIncidencia.html", {"request": MagicMock(), "incidencias": expected_data}
    )

def test_listar_incidencias_html_filter():
    response = client.get("/incidences?status=Resuelto")
    assert response.status_code == 200
    expected_data = [v for v in MockController().data.values() if v.status == "Resuelto"]
    mock_templates.TemplateResponse.assert_called_once_with(
        "ListarIncidencia.html", {"request": MagicMock(), "incidencias": expected_data[:10]}
    )

def test_listar_incidencias_html_error():
    mock_controller.read_all = MagicMock(side_effect=Exception("Error de prueba"))
    response = client.get("/incidences")
    assert response.status_code == 500
    assert response.json()["detail"] == "Error de prueba"
    mock_controller.read_all = MockController().read_all #restaurar

# Tests para /incidences/json
def test_listar_incidencias_json():
    response = client.get("/incidences/json")
    assert response.status_code == 200
    expected_data = [v.dict() for v in MockController().data.values()[:10]]
    assert response.json() == {"data": expected_data}

def test_listar_incidencias_json_pagination():
    response = client.get("/incidences/json?skip=2&limit=2")
    assert response.status_code == 200
    expected_data = [v.dict() for v in list(MockController().data.values())[2:4]]
    assert response.json() == {"data": expected_data}

def test_listar_incidencias_json_filter():
    response = client.get("/incidences/json?status=Resuelto")
    assert response.status_code == 200
    expected_data = [v.dict() for v in MockController().data.values() if v.status == "Resuelto"][:10]
    assert response.json() == {"data": expected_data}

def test_listar_incidencias_json_error():
    mock_controller.read_all = MagicMock(side_effect=Exception("Error de prueba"))
    response = client.get("/incidences/json")
    assert response.status_code == 500
    assert response.json()["detail"] == "Error de prueba"
    mock_controller.read_all = MockController().read_all #restaurar

# Tests para /{incidence_id} (HTML)
def test_obtener_incidencia_html_found():
    response = client.get("/incidences/1")
    assert response.status_code == 200
    expected_incidence = MockController().data[1]
    mock_templates.TemplateResponse.assert_called_once_with(
        "DetalleIncidencia.html", {"request": MagicMock(), "incidencia": expected_incidence}
    )

def test_obtener_incidencia_html_not_found():
    response = client.get("/incidences/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia no encontrada"

def test_obtener_incidencia_html_error():
    mock_controller.get_by_id = MagicMock(side_effect=Exception("Error de prueba"))
    response = client.get("/incidences/1")
    assert response.status_code == 500
    assert response.json()["detail"] == "Error de prueba"
    mock_controller.get_by_id = MockController().get_by_id #restaurar

# Tests para /{incidence_id}/json
def test_obtener_incidencia_json_found():
    response = client.get("/incidences/1/json")
    assert response.status_code == 200
    expected_data = MockController().data[1].dict()
    assert response.json() == {"data": expected_data}

def test_obtener_incidencia_json_not_found():
    response = client.get("/incidences/999/json")
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia no encontrada"

def test_obtener_incidencia_json_error():
    mock_controller.get_by_id = MagicMock(side_effect=Exception("Error de prueba"))
    response = client.get("/incidences/1/json")
    assert response.status_code == 500
    assert response.json()["detail"] == "Error de prueba"
    mock_controller.get_by_id = MockController().get_by_id #restaurar

# Tests para /incidences/consultar
def test_consultar_incidencias_html():
    response = client.get("/incidences/consultar")
    assert response.status_code == 200
    mock_templates.TemplateResponse.assert_called_once_with(
        "ConsultarIncidencia", {"request": MagicMock()}
    )