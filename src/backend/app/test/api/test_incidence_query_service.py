from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.api.routes.incidence_query_service import app as incidence_router

app_for_test = FastAPI()
app_for_test.include_router(incidence_router)
client = TestClient(app_for_test)

def test_consultar_page():
    """Prueba que la ruta '/consultar' devuelve la plantilla 'ConsultarIncidencia.html' correctamente."""
    response = client.get("/incidence/consultar")
    assert response.status_code == 200
    assert "Consultar Incidencia" in response.text

def test_get_all_incidences():
    """Prueba que la ruta '/incidencias' devuelve correctamente todas las incidencias."""
    # Primero, crear algunas incidencias para probar
    client.post(
        "/incidence/create",
        data={"Descripcion": "Incidencia1", "Tipo": "Tipo1", "TicketID": 5}
    )
    client.post(
        "/incidence/create",
        data={"Descripcion": "Incidencia2", "Tipo": "Tipo2", "TicketID": 6}
    )
    response = client.get("/incidence/incidencias")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert data[0]["Descripcion"] in ["Incidencia1", "Incidencia2"]
    assert data[0]["Tipo"] in ["Tipo1", "Tipo2"]

def test_get_incidence_by_id_existing():
    """Prueba que la ruta '/incidencia/{IncidenciaID}' devuelve la incidencia correcta cuando existe."""
    # Primero, crear una incidencia para probar
    create_response = client.post(
        "/incidence/create",
        data={"Descripcion": "FindByIDE", "Tipo": "TipoIDE", "TicketID": 7}
    )
    assert create_response.status_code == 200
    created_data = create_response.json()["data"]
    incidence_id = created_data["IncidenciaID"]

    response = client.get(f"/incidence/incidencia/{incidence_id}")
    assert response.status_code == 200
    assert "FindByIDE" in response.text
    assert "TipoIDE" in response.text
    assert str(incidence_id) in response.text

def test_get_incidence_by_id_not_found():
    """Prueba que la ruta '/incidencia/{IncidenciaID}' devuelve 'None' cuando no encuentra la incidencia."""
    response = client.get("/incidence/incidencia/9999")
    assert response.status_code == 200
    assert "None" in response.text
