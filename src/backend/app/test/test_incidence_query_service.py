import pytest
from httpx import AsyncClient
from fastapi import FastAPI, HTTPException, Request, Query, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from unittest.mock import AsyncMock, MagicMock, patch
from typing import List, Optional

# Asume que estos están en archivos separados
# from backend.app.models.incidence import IncidenceOut
# from logic.universal_controller_sql import UniversalController

# Para simplificar, definimos modelos y controlador mock aquí
class IncidenceOut:
    def __init__(self, incidence_id: int, description: str, type: str, status: str):
        self.incidence_id = incidence_id
        self.description = description
        self.type = type
        self.status = status

    def dict(self):
        return {"id": self.incidence_id, "description": self.description, "type": self.type, "status": self.status}
    
    @staticmethod
    def get_empty_instance():
        return IncidenceOut(incidence_id=None, description=None, type=None, status=None)


class MockController:
    def __init__(self):
        self.data = {
            1: IncidenceOut(incidence_id=1, description="Incidente 1", type="Tipo A", status="abierto"),
            2: IncidenceOut(incidence_id=2, description="Incidente 2", type="Tipo B", status="cerrado"),
            3: IncidenceOut(incidence_id=3, description="Incidente 3", type="Tipo A", status="abierto"),
            4: IncidenceOut(incidence_id=4, description="Incidente 4", type="Tipo C", status="en progreso"),
            5: IncidenceOut(incidence_id=5, description="Incidente 5", type="Tipo B", status="cerrado"),
        }

    async def read_all(self, model) -> List[IncidenceOut]:
        return list(self.data.values())

    async def get_by_id(self, model, incidence_id) -> Optional[IncidenceOut]:
        return self.data.get(incidence_id)


# Crear una instancia de FastAPI para las pruebas
@pytest.fixture
def test_app():
    app = FastAPI()
    # Mock global del controlador
    mock_controller = MockController()

    # Incluir el router con el controlador mock
    app = APIRouter(prefix="/incidences", tags=["incidencias"])

    # Mock de templates
    templates = MagicMock()

    @app.get("", response_class=HTMLResponse)
    async def listar_incidencias_html(
        request: Request,
        skip: int = Query(0, description="Registros a saltar"),
        limit: int = Query(10, description="Límite de resultados"),
        status: Optional[str] = Query(None, description="Filtrar por estado (opcional)")
    ):
        try:
            dummy = IncidenceOut.get_empty_instance()
            all_data = await mock_controller.read_all(dummy)

            # Filtrado por estado (si se especifica)
            if status:
                filtered_data = [item for item in all_data if item.status == status]
            else:
                filtered_data = all_data

            # Paginación
            paginated_data = filtered_data[skip:skip + limit]
            return templates.TemplateResponse("ListarIncidencia.html", {"request": request, "incidencias": paginated_data})
        except Exception as e:
            raise HTTPException(500, detail=str(e))

    # Endpoint 1 (JSON): Obtener todas las incidencias (con paginación y filtro) - JSON
    @app.get("/json")
    async def listar_incidencias_json(
        skip: int = Query(0, description="Registros a saltar"),
        limit: int = Query(10, description="Límite de resultados"),
        status: Optional[str] = Query(None, description="Filtrar por estado (opcional)")
    ):
        try:
            dummy = IncidenceOut.get_empty_instance()
            all_data = await mock_controller.read_all(dummy)

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
            incidence = await mock_controller.get_by_id(IncidenceOut, incidence_id)
            if not incidence:
                raise HTTPException(status_code=404, detail="Incidencia no encontrada")
            return templates.TemplateResponse("DetalleIncidencia.html", {"request": request, "incidencia": incidence})
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(500, detail=str(e))

    # Endpoint 2 (JSON): Obtener incidencia por ID - JSON
    @app.get("/{incidence_id}/json")
    async def obtener_incidencia_json(incidence_id: int = Query(...)):
        try:
            incidence = await mock_controller.get_by_id(IncidenceOut, incidence_id)
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
        return templates.TemplateResponse("ConsultarIncidencia", {"request": request})
    
    app.include_router(app)
    return app



@pytest.mark.asyncio
async def test_listar_incidencias_json(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        response = await ac.get("/incidences/json?skip=0&limit=10")
    
    assert response.status_code == 200
    assert len(response.json()["data"]) <= 10  # Verifica el límite
    assert response.json()["data"][0]["description"] == "Incidente 1"

@pytest.mark.asyncio
async def test_listar_incidencias_json_pagination(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        response = await ac.get("/incidences/json?skip=2&limit=2")
    
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2
    assert response.json()["data"][0]["description"] == "Incidente 3"
    assert response.json()["data"][1]["description"] == "Incidente 4"

@pytest.mark.asyncio
async def test_listar_incidencias_json_filter(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        response = await ac.get("/incidences/json?status=cerrado")
    
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2
    for item in response.json()["data"]:
        assert item["status"] == "cerrado"

@pytest.mark.asyncio
async def test_listar_incidencias_json_empty_result(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        response = await ac.get("/incidences/json?status=no_existe")
    
    assert response.status_code == 200
    assert response.json()["data"] == []

@pytest.mark.asyncio
async def test_obtener_incidencia_json_success(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        response = await ac.get("/incidences/2/json")
    
    assert response.status_code == 200
    assert response.json()["data"]["id"] == 2
    assert response.json()["data"]["status"] == "cerrado"
    assert response.json()["data"]["description"] == "Incidente 2"

@pytest.mark.asyncio
async def test_obtener_incidencia_json_not_found(test_app):
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        response = await ac.get("/incidences/999/json")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia no encontrada"
