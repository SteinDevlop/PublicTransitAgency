
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.api.routes.card_cud_service import app as card_router  # Importa bien
from backend.app.core.conf import headers


# Limpieza de base de datos antes y después de cada test
def setup_function():
    UniversalController().clear_tables()

def teardown_function():
    UniversalController().clear_tables()

# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(card_router)
app_for_test.mount("/static", StaticFiles(directory="src/frontend/static"), name="static")

# Cliente de prueba
client = TestClient(app_for_test)


### 1. PRUEBAS DE AUTENTICACIÓN Y AUTORIZACIÓN ###

def test_create_card_unauthorized():
    |||Verifica que la creación de tarjeta falle sin autenticación|||
    response = client.post("/card/create", data={"id": 15, "tipo": "tipo_1"})
    assert response.status_code == 401  # Debe devolver error 401 por falta de autenticación
    assert "detail" in response.json()  # El detalle debe indicar que se necesita autenticación

def test_update_card_unauthorized():
    |||Verifica que la actualización de tarjeta falle sin autenticación|||
    response = client.post("/card/update", data={"id": 15, "tipo": "tipo_1_updated"})
    assert response.status_code == 401  # Debe devolver error 401 por falta de autenticación
    assert "detail" in response.json()  # El detalle debe indicar que se necesita autenticación

def test_update_card_unauthorized_user():
    |||Verifica que el usuario no autorizado no pueda actualizar una tarjeta de otro|||
    response = client.post("/card/update", data={"id": 999, "tipo": "tipo_no_autorizado"})
    assert response.status_code == 403  # Se debe devolver un error 403 de acceso prohibido
    assert "detail" in response.json()  # El detalle debe indicar que no tiene permisos para modificar esta tarjeta


### 2. PRUEBAS DE INYECCIÓN SQL ###

def test_sql_injection_create():
    |||Verifica que la API esté protegida contra inyecciones SQL al intentar crear una tarjeta|||
    malicious_payload = "' OR 1=1 --"
    response = client.post("/card/create", data={"id": malicious_payload, "tipo": "tipo_1"}, headers=headers)
    assert response.status_code == 400  # Debe fallar con error 400, ya que no es un ID válido
    assert "detail" in response.json()  # Debe devolver un error indicando que la entrada es inválida

def test_sql_injection_get():
    |||Verifica que la API esté protegida contra inyecciones SQL al intentar obtener una tarjeta|||
    malicious_id = "' OR 1=1 --"
    response = client.get(f"/card/{malicious_id}", headers=headers)
    assert response.status_code == 400  # El resultado debe ser un error 400, no un acceso exitoso
    assert "detail" in response.json()  # El detalle debe indicar que la solicitud fue malformada


### 3. PRUEBAS DE XSS (CROSS-SITE SCRIPTING) ###

def test_xss_create_card():
    |||Verifica que no sea posible inyectar scripts maliciosos en los parámetros al crear una tarjeta|||
    malicious_payload = "<script>alert('XSS')</script>"
    response = client.post("/card/create", data={"id": 15, "tipo": malicious_payload}, headers=headers)
    assert response.status_code == 200  # La creación debe ser exitosa, pero el payload no debe ser ejecutado
    json_data = response.json()
    assert malicious_payload not in json_data["tipo"]  # El payload malicioso no debe estar en la respuesta

def test_xss_get_card():
    |||Verifica que no sea posible inyectar scripts maliciosos en los parámetros al obtener una tarjeta|||
    malicious_id = "<script>alert('XSS')</script>"
    response = client.get(f"/card/{malicious_id}", headers=headers)
    assert response.status_code == 400  # Debe devolver error 400 debido a la inyección maliciosa
    assert "detail" in response.json()  # La respuesta debe indicar que no se puede obtener la tarjeta

def test_xss_update_card():
    |||Verifica que no se pueda inyectar JavaScript malicioso en el campo de tipo al actualizar una tarjeta|||
    malicious_payload = "<script>alert('XSS')</script>"
    response = client.post("/card/update", data={"id": 15, "tipo": malicious_payload}, headers=headers)
    assert response.status_code == 200  # La actualización debe ser exitosa, pero el payload no debe ser ejecutado
    json_data = response.json()
    assert malicious_payload not in json_data["tipo"]  # El payload malicioso no debe ser reflejado en la respuesta
"""