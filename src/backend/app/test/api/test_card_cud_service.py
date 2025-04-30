from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.api.routes.card_cud_service import app as card_router  # Importa bien
# Limpieza de base de datos antes y después de cada test
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()
# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(card_router)

# Cliente de prueba
client = TestClient(app_for_test)

def test_create_card():
    response = client.post("/card/create", data={"id": 15, "tipo": "tipo_1"})
    assert response.status_code == 200

def test_update_card_existing():
    # Crear el registro primero
    client.post("/card/create", data={"id": 15, "tipo": "tipo_original"})
    
    # Luego actualizarlo
    response = client.post("/card/update", data={"id": 15, "tipo": "tipo_1_updated"})
    assert response.status_code == 200

def test_update_card_not_found():
    response = client.post("/card/update", data={"id": 999, "tipo": "tipo_nonexistent"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"

def test_delete_card_existing():
    # Crear el registro primero
    client.post("/card/create", data={"id": 15, "tipo": "tipo_para_borrar"})
    
    # Luego eliminarlo
    response = client.post("/card/delete", data={"id": 15})
    assert response.status_code == 200
def test_delete_card_not_found():
    response = client.post("/card/delete", data={"id": 999})
    assert response.status_code == 404
    assert response.json()["detail"] == "Card not found"

def test_index_create_form():
    response = client.get("/card/crear")
    assert response.status_code == 200

def test_index_update_form():
    response = client.get("/card/actualizar")
    assert response.status_code == 200

def test_index_delete_form():
    response = client.get("/card/eliminar")
    assert response.status_code == 200
