from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.card_query_service import app as card_router  # Importa bien
import pytest
from fastapi.staticfiles import StaticFiles
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.card import CardCreate, CardOut
from backend.app.test.conf import headers
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

@pytest.fixture(autouse=True)
def setup_db():
    # Crea las tarjetas necesarias antes de cada test
    uc = UniversalController()

    # Limpiar las tablas antes de cada test
    uc.clear_tables()

    # Insertar tarjetas para la prueba
    uc.add(CardCreate(id=3, tipo="tipo_3", balance=0.0))
    uc.add(CardCreate(id=4, tipo="tipo_4", balance=10.0))
    uc.add(CardCreate(id=2, tipo="tipo_2", balance=5.0))
    uc.add(CardCreate(id=1, tipo="tipo_1", balance=0.0))

# Crear la aplicación de prueba
app_for_test = FastAPI()
app_for_test.include_router(card_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
# Cliente de prueba
client = TestClient(app_for_test)

def test_consultar_page():
    """Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarTarjeta.html' correctamente."""
    response = client.get("/card/consultar",headers=headers)
    assert response.status_code == 200
    assert "Consultar Saldo" in response.text  # Verifica si la plantilla está presente

def test_get_tarjetas():
    """Prueba que la ruta '/tarjetas' devuelve correctamente todas las tarjetas."""
    response = client.get("/card/tarjetas",headers=headers)
    assert response.status_code == 200
    data = response.json()  # Asegúrate de que la respuesta esté en formato JSON
    assert len(data) == 4  # Ahora esperamos 4 tarjetas
    assert data[0]["id"] == 1
    assert data[1]["tipo"] == "tipo_2"
    assert data[2]["id"] == 3
    assert data[3]["tipo"] == "tipo_4"

def test_get_tarjeta_existing():
    """Prueba que la ruta '/tarjeta' devuelve la tarjeta correctamente cuando existe."""
    response = client.get("/card/tarjeta?id=3",headers=headers)
    assert response.status_code == 200
    assert "tipo_3" in response.text  # Verifica si el tipo de tarjeta está en el HTML
    assert "0.0" in response.text  # Verifica si el saldo está en el HTML

def test_get_tarjeta_not_found():
    """Prueba que la ruta '/tarjeta' devuelve un valor 'None' cuando no encuentra la tarjeta."""
    response = client.get("/card/tarjeta?id=9999",headers=headers)  # ID que no existe
    assert response.status_code == 200
    assert "None" in response.text  # Verifica si el tipo de tarjeta está en el HTML
    assert "None" in response.text  # Verifica si el saldo está en el HTML
