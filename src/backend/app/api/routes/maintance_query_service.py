from fastapi import APIRouter, HTTPException, Security
from backend.app.logic.mantainment_controller import Controller
from backend.app.core.auth import get_current_user
from fastapi import Form

# Initialize the maintenance controller
controller_maintenance = Controller()

# Create the APIRouter instance with a prefix and tags
app = APIRouter(prefix="/maintainance", tags=["maintainance"])


@app.get("/maintainancements", response_model=list[dict])
def get_all(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "mantenimiento"])
):
    """
    Returns all maintenance records.

    Args:
    - current_user (dict): User information from authentication.

    Returns:
    - List of maintenance records.
    """
    return controller_maintenance.get_all()


@app.get("/{id}")
def get_by_id(
    id: int,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "mantenimiento"])
):
    """
    Returns a maintenance record by its ID.
    If not found, raises a 404 error.

    Args:
    - id (int): The ID of the maintenance record.
    - current_user (dict): User information from authentication.

    Returns:
    - The maintenance record in dictionary format.

    Raises:
    - HTTPException: If the maintenance record is not found.
    """
    result = controller_maintenance.get_by_id(id)
    if not result:
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    return result.to_dict()


@app.get("/unit/{unit_id}")
def get_by_unit(
    unit_id: int,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "mantenimiento"])
):
    """
    Returns all maintenance records associated with a specific unit.

    Args:
    - unit_id (int): The ID of the unit.
    - current_user (dict): User information from authentication.

    Returns:
    - List of maintenance records associated with the unit.
    """
    return controller_maintenance.get_by_unit(unit_id)
