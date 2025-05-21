from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.api.routes.pqr_service import pqr_cud_service  # Importamos el módulo, no solo el `app`
from backend.app.core.conf import headers
from backend.app.models.pqr import PQRCreate, PQROut

# App de prueba
app_for_test = FastAPI()
app_for_test.include_router(pqr_cud_service.app)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

client = TestClient(app_for_test)

def test_create_pqr():
    response = client.post("/pqr/create", data={"ID": 44, "identificationuser": 33, "type":"none","description":"aaa",
                                                 "fecha":"29-08-2024"}, headers=headers)
    assert response.status_code == 200

def test_update_pqr_existing():
    response = client.post("/pqr/update", data={"ID": 44, "identificationuser": 33, "type":"none", "description":"aaa",
                                                "fecha":"29-08-2024"}, 
                           headers=headers)
    assert response.status_code == 200

def test_update_pqr_not_found():
    response = client.post("/pqr/update", data={"ID": 999, "identificationuser": 33, "type":"bb", "description":"aaa",
                                                "fecha":"29-08-2024"}, headers=headers)
    assert response.status_code == 404

def test_delete_pqr_existing():
    response = client.post("/pqr/delete", data={"ID": 44}, headers=headers)
    assert response.status_code == 200

def test_delete_pqr_not_found():
    response = client.post("/pqr/delete", data={"ID": 999}, headers=headers)
    assert response.status_code == 404

def test_index_create_form():
    response = client.get("/pqr/administrador/crear", headers=headers)
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/pqr/administrador/actualizar", headers=headers)
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/pqr/administrador/eliminar", headers=headers)
    assert response.status_code == 200
