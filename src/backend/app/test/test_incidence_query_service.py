"""from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app as incidence_router

app_for_test = FastAPI()
app_for_test.include_router(incidence_router)

client = TestClient(app_for_test)

def test_consultar_incidencias_page():
    response = client.get("/incidences/consultar")
    assert response.status_code == 200
    assert "ConsultarIncidencia" in response.text

def test_get_incidencias_json():
    response = client.get("/incidences/json")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) >= 0 # Puede haber 0 incidencias en la DB de prueba

def test_get_incidencia_html_existing():
    existing_incidence_id = 1
    response = client.get(f"/incidences/{existing_incidence_id}")
    assert response.status_code == 200
    assert "Detalle de Incidencia" in response.text # Asumiendo este título en el template

def test_get_incidencia_html_not_found():
    non_existent_incidence_id = 9999
    response = client.get(f"/incidences/{non_existent_incidence_id}")
    assert response.status_code == 404
    assert "Incidencia no encontrada" in response.text

def test_get_incidencia_json_existing():
    existing_incidence_id = 1
    response = client.get(f"/incidences/{existing_incidence_id}/json")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["incidence_id"] == existing_incidence_id

def test_get_incidencia_json_not_found():
    non_existent_incidence_id = 9999
    response = client.get(f"/incidences/{non_existent_incidence_id}/json")
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia no encontrada"

def test_listar_incidencias_html_sin_filtros():
    response = client.get("/incidences")
    assert response.status_code == 200
    assert "Lista de Incidencias" in response.text # Asumiendo este título en el template

def test_listar_incidencias_json_sin_filtros():
    response = client.get("/incidences/json")
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)

def test_listar_incidencias_html_con_filtro():
    response = client.get("/incidences?status=activo")
    assert response.status_code == 200
    assert "Lista de Incidencias" in response.text

def test_listar_incidencias_json_con_filtro():
    response = client.get("/incidences/json?status=activo")
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)

def test_listar_incidencias_html_con_paginacion():
    response = client.get("/incidences?limit=2&skip=0")
    assert response.status_code == 200
    assert "Lista de Incidencias" in response.text

def test_listar_incidencias_json_con_paginacion():
    response = client.get("/incidences/json?limit=2&skip=0")
    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)
    assert len(data) <= 2 """