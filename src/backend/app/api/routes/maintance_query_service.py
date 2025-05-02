import logging
from fastapi import APIRouter, HTTPException, Security
from backend.app.logic.mantainment_controller import Controller
from backend.app.core.auth import get_current_user

# Initialize the maintenance controller
controller_maintenance = Controller()

# Create the APIRouter instance with a prefix and tags
app = APIRouter(prefix="/maintainance", tags=["maintainance"])

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


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
    logger.info(f"[GET /maintainancements] Usuario {current_user['user_id']} accede a todos los registros de mantenimiento.")
    
    try:
        records = controller_maintenance.get_all()
        logger.info(f"[GET /maintainancements] Se han recuperado {len(records)} registros de mantenimiento.")
        return records
    except Exception as e:
        logger.error(f"[GET /maintainancements] Error al obtener los registros de mantenimiento: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


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
    logger.info(f"[GET /{id}] Usuario {current_user['user_id']} busca el mantenimiento con ID {id}.")
    
    result = controller_maintenance.get_by_id(id)
    if not result:
        logger.warning(f"[GET /{id}] Mantenimiento con ID {id} no encontrado.")
        raise HTTPException(status_code=404, detail="Maintenance record not found")
    
    logger.info(f"[GET /{id}] Se ha encontrado el mantenimiento con ID {id}.")
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
    logger.info(f"[GET /unit/{unit_id}] Usuario {current_user['user_id']} busca los mantenimientos asociados a la unidad {unit_id}.")
    
    try:
        records = controller_maintenance.get_by_unit(unit_id)
        logger.info(f"[GET /unit/{unit_id}] Se han recuperado {len(records)} registros de mantenimiento para la unidad {unit_id}.")
        return records
    except Exception as e:
        logger.error(f"[GET /unit/{unit_id}] Error al obtener los registros de mantenimiento para la unidad {unit_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
