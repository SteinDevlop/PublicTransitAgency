import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException, APIRouter
from src.backend.app.logic.mantainment_controller import Controller

# Crear la aplicación FastAPI y las rutas
app = FastAPI()

controller_maintenance = Controller()

# Definir las rutas
router = APIRouter(prefix="/maintainance", tags=["maintainance"])

# Ruta para obtener todos los mantenimientos
@router.get("/maintainancements", response_model=list[dict])
def get_all():
    return controller_maintenance.get_all()

# Ruta para obtener mantenimiento por ID
@router.get("/{id}")
def get_by_id(id: int):
    result = controller_maintenance.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result

# Ruta para obtener mantenimiento por unidad
@router.get("/unit/{unit_id}")
def get_by_unit(unit_id: int):
    return controller_maintenance.get_by_unit(unit_id)

# Registrar las rutas en la app de FastAPI
app.include_router(router)

# Mock de la clase Controller
class MockController:
    def __init__(self):
        # Datos simulados de mantenimiento
        self.maintenances = {
            1: {"id": 1, "unit_id": 101, "status": "completed"},
            2: {"id": 2, "unit_id": 102, "status": "in-progress"}
        }

    def get_all(self):
        """Simula la lectura de todos los registros de mantenimiento."""
        return list(self.maintenances.values())

    def get_by_id(self, id_: int):
        """Simula la obtención de un registro de mantenimiento por ID."""
        return self.maintenances.get(id_)

    def get_by_unit(self, unit_id: int):
        """Simula la obtención de registros de mantenimiento por ID de unidad."""
        return [maintenance for maintenance in self.maintenances.values() if maintenance["unit_id"] == unit_id]

# Reemplazamos el controlador real por el mock en el objeto 'app'
app.dependency_overrides[Controller] = MockController

# Inicializamos el cliente de pruebas de FastAPI
client = TestClient(app)

# Pruebas
@pytest.fixture
def mock_controller():
    """Fixture para el mock del controlador"""
    return MockController()

def test_get_all(mock_controller):
    """Prueba que la ruta '/maintainance/maintainancements' devuelve correctamente todos los registros de mantenimiento."""
    response = client.get("/maintainance/maintainancements")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Esperamos que haya 2 registros en el mock
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2

def test_get_by_id_existing(mock_controller):
    """Prueba que la ruta '/maintainance/{id}' devuelve el registro de mantenimiento cuando existe."""
    response = client.get("/maintainance/1")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"
    
def test_get_by_id_not_found(mock_controller):
    """Prueba que la ruta '/maintainance/{id}' devuelve un error 404 cuando no se encuentra el registro."""
    response = client.get("/maintainance/999")  # ID que no existe
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}

def test_get_by_unit(mock_controller):
    """Prueba que la ruta '/maintainance/unit/{unit_id}' devuelve correctamente los registros de mantenimiento por ID de unidad."""
    response = client.get("/maintainance/unit/101")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1  # Esperamos que haya 1 registro para la unidad 101
    assert data[0]["unit_id"] == 101
    
    response_empty = client.get("/maintainance/unit/999")  # Unidad que no existe
    assert response_empty.status_code == 200
    assert len(response_empty.json()) == 0
