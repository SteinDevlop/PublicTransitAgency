import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from unittest.mock import AsyncMock, MagicMock, patch
from backend.app.models.incidence import IncidenceOut
from backend.app.api.routes.incidence_query_service import app as incidences_router

@pytest.fixture
def test_app():
    app = FastAPI()
    app.include_router(incidences_router)
    return app

@pytest.mark.asyncio
async def test_listar_incidencias_json(test_app):
    mock_data = [
        IncidenceOut(id=1, description="Incidente 1", status="abierto"),
        IncidenceOut(id=2, description="Incidente 2", status="cerrado")
    ]

    with patch("backend.app.api.incidences.controller") as mock_controller:
        mock_controller.read_all.return_value = mock_data

        async with AsyncClient(app=test_app, base_url="http://test") as ac:
            response = await ac.get("/incidences/json?skip=0&limit=10")
        
        assert response.status_code == 200
        assert response.json()["data"][0]["description"] == "Incidente 1"

@pytest.mark.asyncio
async def test_obtener_incidencia_json_success(test_app):
    mock_incidencia = IncidenceOut(id=123, description="Prueba", status="abierto")

    with patch("backend.app.api.incidences.controller") as mock_controller:
        mock_controller.get_by_id.return_value = mock_incidencia

        async with AsyncClient(app=test_app, base_url="http://test") as ac:
            response = await ac.get("/incidences/123/json")

        assert response.status_code == 200
        assert response.json()["data"]["id"] == 123
        assert response.json()["data"]["status"] == "abierto"

@pytest.mark.asyncio
async def test_obtener_incidencia_json_not_found(test_app):
    with patch("backend.app.api.incidences.controller") as mock_controller:
        mock_controller.get_by_id.return_value = None

        async with AsyncClient(app=test_app, base_url="http://test") as ac:
            response = await ac.get("/incidences/999/json")

        assert response.status_code == 404
        assert response.json()["detail"] == "Incidencia no encontrada"
