import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi.staticfiles import StaticFiles

from backend.app.api.routes.type_transport_service.type_transport_query_service import router as typetransport_router
from backend.app.core.conf import headers

test_app = FastAPI()
test_app.include_router(typetransport_router)
test_app.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(test_app)

def test_consultar_page():
    response = client.get("/typetransport/consultar", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "tipo de transporte" in data["message"]

def test_read_all():
    response = client.get("/typetransport/typetransports", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "typetransports" in data
    assert isinstance(data["typetransports"], list)
    # Puedes ajustar este número dependiendo del fixture de tu base de datos de pruebas:
    # assert len(data["typetransports"]) == 6

def test_get_by_id():
    response = client.get("/typetransport/tipotransporte?id=2", headers=headers)
    if response.status_code == 200:
        data = response.json()
        assert data["ID"] == 2
        assert "TipoTransporte" in data
    else:
        # Si no existe, debe retornar 404 y el mensaje adecuado
        assert response.status_code == 404
        assert response.json()["detail"] == "Tipo de transporte no encontrado"

def test_get_by_id_not_found():
    response = client.get("/typetransport/tipotransporte?id=999", headers=headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "Tipo de transporte no encontrado"}