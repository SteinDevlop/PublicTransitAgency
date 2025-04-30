from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app as incidence_query_router # Importa el router
from backend.app.logic import universal_controller_sql as UniversalController
from backend.app.models.incidence import IncidenceOut

# Creamos la app de prueba
app_for_test = FastAPI()
app_for_test.include_router(incidence_query_router)

# Cliente de prueba
client = TestClient(app_for_test)

# Instancia del UniversalController (podrías mockear la base de datos)
controller = UniversalController()

# Asegurarse de que la tabla existe
dummy_incidence = IncidenceOut.get_empty_instance()
controller._ensure_table_exists(dummy_incidence)

# Datos de prueba (simulando que ya existen en la base de datos)
test_incidences = [
    {"incidence_id": 1, "description": "Fallo A", "type": "Crítico", "status": "activo"},
    {"incidence_id": 2, "description": "Problema B", "type": "Medio", "status": "pendiente"},
    {"incidence_id": 3, "description": "Error C", "type": "Bajo", "status": "activo"},
    {"incidence_id": 4, "description": "Solicitud D", "type": "Medio", "status": "completado"},
    {"incidence_id": 5, "description": "Fallo E", "type": "Crítico", "status": "activo"},
]

# Función para poblar la base de datos de prueba (esto en una prueba real se haría con mocks)
def populate_database():
    for incidence_data in test_incidences:
        incidence = IncidenceOut(**incidence_data)
        try:
            controller.add(incidence)
        except ValueError:
            # Si ya existe, lo ignoramos para las pruebas repetidas
            pass

populate_database()

def test_listar_incidencias_html_sin_filtros():
    response = client.get("/incidences")
    assert response.status_code == 200
    assert "Fallo A" in response.text
    assert "Problema B" in response.text

def test_listar_incidencias_html_con_filtro():
    response = client.get("/incidences?status=activo")
    assert response.status_code == 200
    assert "Fallo A" in response.text
    assert "Problema B" not in response.text
    assert "Error C" in response.text

def test_listar_incidencias_html_con_paginacion():
    response = client.get("/incidences?limit=2&skip=1")
    assert response.status_code == 200
    assert "Fallo A" not in response.text
    assert "Problema B" in response.text
    assert "Error C" in response.text
    assert response.text.count("<tr>") == 3 # Incluye la cabecera de la tabla

def test_listar_incidencias_json_sin_filtros():
    response = client.get("/incidences/json")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 5

def test_listar_incidencias_json_con_filtro():
    response = client.get("/incidences/json?status=pendiente")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["description"] == "Problema B"

def test_listar_incidencias_json_con_paginacion():
    response = client.get("/incidences/json?limit=2&skip=2")
    assert response.status_code == 200
    assert len(response.json()["data"]) == 2
    assert response.json()["data"][0]["description"] == "Error C"
    assert response.json()["data"][1]["description"] == "Solicitud D"

def test_obtener_incidencia_html_existente():
    response = client.get("/incidences/1")
    assert response.status_code == 200
    assert "Fallo A" in response.text

def test_obtener_incidencia_html_no_existente():
    response = client.get("/incidences/999")
    assert response.status_code == 404
    assert "Incidencia no encontrada" in response.text # Verifica el mensaje de error en HTML

def test_obtener_incidencia_json_existente():
    response = client.get("/incidences/1/json")
    assert response.status_code == 200
    assert response.json()["data"]["description"] == "Fallo A"

def test_obtener_incidencia_json_no_existente():
    response = client.get("/incidences/999/json")
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia no encontrada"

def test_consultar_incidencias_form():
    response = client.get("/incidences/consultar")
    assert response.status_code == 200
    assert "ConsultarIncidencia" in response.text # Verifica el nombre del template (o algún contenido distintivo)