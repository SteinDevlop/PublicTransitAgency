"""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.card_query_service import app as card_router  # Importa bien
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.card import CardCreate, CardOut
from fastapi.staticfiles import StaticFiles
from backend.app.core.conf import headers


# Limpieza de base de datos antes y después de cada test
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()


@pytest.fixture(autouse=True)
def setup_db():
    |||Prepara la base de datos con tarjetas necesarias antes de cada test|||
    uc = UniversalController()
    uc.clear_tables()
    # Inserta algunas tarjetas para las pruebas
    uc.add(CardCreate(id=3, tipo="tipo_3", balance=0.0))
    uc.add(CardCreate(id=4, tipo="tipo_4", balance=10.0))
    uc.add(CardCreate(id=2, tipo="tipo_2", balance=5.0))
    uc.add(CardCreate(id=1, tipo="tipo_1", balance=0.0))


# Crear la aplicación de prueba
app_for_test = FastAPI()
app_for_test.include_router(card_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")
client = TestClient(app_for_test)


### 1. PRUEBAS DE AUTORIZACIÓN ###

def test_get_tarjetas_unauthorized():
    |||Verifica que la ruta '/tarjetas' falle sin autorización (sin el encabezado de autenticación).|||
    response = client.get("/card/tarjetas")
    assert response.status_code == 401  # Debe devolver un error 401 (Unauthorized)
    assert "detail" in response.json()  # Detalle debe indicar que falta la autenticación


def test_get_tarjeta_unauthorized():
    |||Verifica que la ruta '/tarjeta' falle sin autorización (sin el encabezado de autenticación).|||
    response = client.get("/card/tarjeta?id=1")
    assert response.status_code == 401  # Debe devolver un error 401 (Unauthorized)
    assert "detail" in response.json()  # Detalle debe indicar que falta la autenticación


### 2. PRUEBAS DE INYECCIÓN SQL ###

def test_sql_injection_get_tarjetas():
    |||Verifica que la ruta '/tarjetas' esté protegida contra inyecciones SQL.|||
    malicious_payload = "' OR 1=1 --"
    response = client.get(f"/card/tarjetas?id={malicious_payload}", headers=headers)
    assert response.status_code == 400  # La inyección debe fallar y devolver un error 400
    assert "detail" in response.json()  # Detalle debe indicar que la solicitud es malformada

def test_sql_injection_get_tarjeta():
    |||Verifica que la ruta '/tarjeta' esté protegida contra inyecciones SQL.|||
    malicious_payload = "' OR 1=1 --"
    response = client.get(f"/card/tarjeta?id={malicious_payload}", headers=headers)
    assert response.status_code == 400  # La inyección debe fallar y devolver un error 400
    assert "detail" in response.json()  # Detalle debe indicar que la solicitud es malformada


### 3. PRUEBAS DE XSS (CROSS-SITE SCRIPTING) ###

def test_xss_injection_get_tarjetas():
    |||Verifica que la API esté protegida contra XSS al intentar inyectar código JavaScript en los parámetros|||
    malicious_payload = "<script>alert('XSS')</script>"
    response = client.get(f"/card/tarjetas?id={malicious_payload}", headers=headers)
    assert response.status_code == 400  # Debe devolver un error 400 porque el parámetro es malicioso
    assert "detail" in response.json()  # Detalle debe indicar que la solicitud está malformada

def test_xss_injection_get_tarjeta():
    |||Verifica que la API esté protegida contra XSS al intentar inyectar código JavaScript en los parámetros|||
    malicious_payload = "<script>alert('XSS')</script>"
    response = client.get(f"/card/tarjeta?id={malicious_payload}", headers=headers)
    assert response.status_code == 400  # Debe devolver un error 400 debido a la inyección de XSS
    assert "detail" in response.json()  # Detalle debe indicar que la solicitud está malformada
    """