from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.backend.app.api.routes.card_query_service import app as card_router  # Importa bien

# Crear la aplicación de prueba
app_for_test = FastAPI()
app_for_test.include_router(card_router)

# Cliente de prueba
client = TestClient(app_for_test)

def test_consultar_page():
    """Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarTarjeta.html' correctamente."""
    response = client.get("/card/consultar")
    assert response.status_code == 200
    assert "Consultar Saldo" in response.text  # Verifica si la plantilla está presente
def test_get_tarjetas():
    """Prueba que la ruta '/tarjetas' devuelve correctamente todas las tarjetas."""
    response = client.get("/card/tarjetas")
    assert response.status_code == 200
    data = response.json()  # Asegúrate de que la respuesta esté en formato JSON
    assert len(data) == 4  # Hay 4 tarjetas, no 2
    assert data[0]["id"] == 3
    assert data[1]["tipo"] == "Tren"
    assert data[2]["id"] == 91
    assert data[3]["tipo"] == "tipo_3"

def test_get_tarjeta_existing():
    """Prueba que la ruta '/tarjeta' devuelve la tarjeta correctamente cuando existe."""
    response = client.get("/card/tarjeta?id=3")
    assert response.status_code == 200
    assert "tipo_3" in response.text  # Verifica si el tipo de tarjeta está en el HTML
    assert "0.0" in response.text  # Verifica si el saldo está en el HTML
def test_get_tarjeta_not_found():
    """Prueba que la ruta '/tarjeta' devuelve un valor 'None' cuando no encuentra la tarjeta."""
    response = client.get("/card/tarjeta?id=9999")  # ID que no existe
    assert response.status_code == 200
    assert "None" in response.text  # Verifica si el tipo de tarjeta está en el HTML
    assert "None" in response.text  # Verifica si el saldo está en el HTML

