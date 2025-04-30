
"""
from fastapi import FastAPI, Form, HTTPException
from fastapi.testclient import TestClient
import pytest
from unittest.mock import MagicMock

# Asume que estos están en archivos separados
from models.incidence import IncidenceCreate, IncidenceOut
from logic.universal_controller_sql import UniversalController

# Crear una instancia de FastAPI para las pruebas
app_for_test = FastAPI()

# Mock del Controlador
class MockController:
    def __init__(self):
        self.data = {}
        self.next_id = 1

    def add(self, incidence_dict):
        incidence_id = incidence_dict.get("incidence_id")  # Usar get() para manejar None
        if not incidence_id:
            incidence_id = self.next_id
            self.next_id += 1
        incidence_dict["incidence_id"] = incidence_id
        self.data[incidence_id] = incidence_dict
        return IncidenceOut(**incidence_dict)

    def get_by_id(self, model, incidence_id):
        if incidence_id in self.data:
            return IncidenceOut(**self.data[incidence_id])
        return None

    def update(self, incidence_dict):
        if incidence_dict["incidence_id"] not in self.data:
            return None  # Simula no encontrado
        self.data[incidence_dict["incidence_id"]] = incidence_dict
        return IncidenceOut(**incidence_dict)

    def delete(self, instance):
        if instance.incidence_id not in self.data:
            return False
        del self.data[instance.incidence_id]
        return True

# Incluimos las rutas directamente, usando el controlador mock
app_for_test.dependency_overrides[UniversalController] = lambda: MockController()  # Inyectar mock

@app_for_test.post("/incidence/create")
async def create_incidence(
    description: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    incidence_id: int = Form(None),
):
    try:
        incidence = IncidenceCreate(
            description=description,
            type=type,
            status=status,
            incidence_id=incidence_id,
        )
        result = MockController().add(incidence.to_dict()) #llamamos al mock
        return {
            "operation": "create",
            "data": result.dict(),
            "message": "Incidencia creada exitosamente",
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app_for_test.post("/incidence/update")
async def update_incidence(
    incidence_id: int = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
):
    try:
        existing = MockController().get_by_id(IncidenceOut, incidence_id) #llamamos al mock
        if not existing:
            raise HTTPException(404, detail="Incidencia no encontrada")
        updated = IncidenceCreate(
            incidence_id=incidence_id,
            description=description,
            type=type,
            status=status,
        )
        result = MockController().update(updated.to_dict()) #llamamos al mock
        return {
            "operation": "update",
            "data": result.dict(),
            "message": f"Incidencia {incidence_id} actualizada",
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))



@app_for_test.post("/incidence/delete")
async def delete_incidence(incidence_id: int = Form(...)):
    existing = MockController().get_by_id(IncidenceOut, incidence_id) #llamamos al mock
    if not existing:
        raise HTTPException(404, detail="Incidencia no encontrada")
    MockController().delete(existing) #llamamos al mock
    return {
        "operation": "delete",
        "message": f"Incidencia {incidence_id} eliminada",
    }


# Cliente de prueba
client = TestClient(app_for_test)

# Tests para /incidence/create
def test_create_incidence_success():
    response = client.post(
        "/incidence/create",
        data={
            "description": "Descripción de prueba",
            "type": "Tipo de prueba",
            "status": "Estado de prueba",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["operation"] == "create"
    assert body["message"] == "Incidencia creada exitosamente"
    assert body["data"]["description"] == "Descripción de prueba"
    assert body["data"]["type"] == "Tipo de prueba"
    assert body["data"]["status"] == "Estado de prueba"
    assert body["data"]["incidence_id"] == 1

def test_create_incidence_invalid_input():
    response = client.post("/incidence/create", data={})
    assert response.status_code == 422
    assert "detail" in response.json()

def test_create_incidence_value_error():
    # Mockear el controlador para que lance un ValueError
    mock_controller = MagicMock()
    mock_controller.add.side_effect = ValueError("Error de valor de prueba")
    app_for_test.dependency_overrides[UniversalController] = lambda: mock_controller #inyectamos el mock

    response = client.post(
        "/incidence/create",
        data={
            "description": "Descripción de prueba",
            "type": "Tipo de prueba",
            "status": "Estado de prueba",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Error de valor de prueba"
    app_for_test.dependency_overrides = {}  # Limpiar override



# Tests para /incidence/update
def test_update_incidence_success():
    # Primero, crear una incidencia para actualizar
    client.post(
        "/incidence/create",
        data={
            "description": "Descripción inicial",
            "type": "Tipo inicial",
            "status": "Estado inicial",
        },
    )
    # Luego, actualizarla
    response = client.post(
        "/incidence/update",
        data={
            "incidence_id": 1,
            "description": "Descripción actualizada",
            "type": "Tipo actualizado",
            "status": "Estado actualizado",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["operation"] == "update"
    assert body["message"] == "Incidencia 1 actualizada"
    assert body["data"]["description"] == "Descripción actualizada"
    assert body["data"]["type"] == "Tipo actualizado"
    assert body["data"]["status"] == "Estado actualizado"
    assert body["data"]["incidence_id"] == 1

def test_update_incidence_not_found():
    response = client.post(
        "/incidence/update",
        data={
            "incidence_id": 999,  # ID que no existe
            "description": "Descripción actualizada",
            "type": "Tipo actualizado",
            "status": "Estado actualizado",
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia no encontrada"

def test_update_incidence_invalid_input():
    response = client.post(
        "/incidence/update",
        data={
            "incidence_id": 1,
        },
    )
    assert response.status_code == 422
    assert "detail" in response.json()

def test_update_incidence_value_error():
    # Mockear el controlador para lanzar ValueError
    mock_controller = MagicMock()
    mock_controller.update.side_effect = ValueError("Error de valor al actualizar")
    app_for_test.dependency_overrides[UniversalController] = lambda: mock_controller #inyectamos mock

    # Primero, crear una incidencia para poder actualizarla
    client.post(
        "/incidence/create",
        data={
            "description": "Descripción inicial",
            "type": "Tipo inicial",
            "status": "Estado inicial",
        },
    )

    response = client.post(
        "/incidence/update",
        data={
            "incidence_id": 1,
            "description": "Descripción actualizada",
            "type": "Tipo actualizado",
            "status": "Estado actualizado",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Error de valor al actualizar"
    app_for_test.dependency_overrides = {}

# Tests para /incidence/delete
def test_delete_incidence_success():
    # Primero, crear una incidencia para eliminar
    client.post(
        "/incidence/create",
        data={
            "description": "Descripción inicial",
            "type": "Tipo inicial",
            "status": "Estado inicial",
        },
    )
    response = client.post(
        "/incidence/delete",
        data={
            "incidence_id": 1,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["operation"] == "delete"
    assert body["message"] == "Incidencia 1 eliminada"

def test_delete_incidence_not_found():
    response = client.post(
        "/incidence/delete",
        data={
            "incidence_id": 999,  # ID que no existe
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Incidencia no encontrada"

def test_delete_incidence_value_error():
    mock_controller = MagicMock()
    mock_controller.get_by_id.return_value = MagicMock() #simula que existe la incidencia
    mock_controller.delete.side_effect = ValueError("Error de valor al eliminar")
    app_for_test.dependency_overrides[UniversalController] = lambda: mock_controller #inyectamos mock
    
    response = client.post(
        "/incidence/delete",
        data={
            "incidence_id": 1,  # ID que existe
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Error de valor al eliminar"
    app_for_test.dependency_overrides = {}"""