import logging
from fastapi import APIRouter, HTTPException, Security,Request
from fastapi.responses import HTMLResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user
from backend.app.models.maintainance import MaintenanceOut
from fastapi.templating import Jinja2Templates

# Initialize the maintenance controller


# Create the APIRouter instance with a prefix and tags
app = APIRouter(prefix="/maintainance", tags=["maintainance"])
# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/maintainancements", response_model=list[dict])
def read_all():
    """
    Returns all maintenance records.

    Args:
    - current_user (dict): User information from authentication.

    Returns:
    - List of maintenance records.
    """
    
    try:
        records = controller.read_all(MaintenanceOut)
        logger.info(f"[GET /maintainancements] Se han recuperado {len(records)} registros de mantenimiento.")
        return records
    except Exception as e:
        logger.error(f"[GET /maintainancements] Error al obtener los registros de mantenimiento: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/id/{ID}")
def get_by_id(
    ID: int
    
):
    """
    Returns a maintenance record by its ID.
    If not found, raises a 404 error.

    Args:
    - ID (int): The ID of the maintenance record.
    - current_user (dict): User information from authentication.

    Returns:
    - The maintenance record in dictionary format.

    Raises:
    - HTTPException: If the maintenance record is not found.
    """    
    result = controller.get_by_id(MaintenanceOut,ID)
    if not result:
        logger.warning(f"[GET /{ID}] Mantenimiento con ID {ID} no encontrado.")
        raise HTTPException(status_code=404, detail="Not found")
    
    logger.info(f"[GET /{ID}] Se ha encontrado el mantenimiento con ID {ID}.")
    return result.to_dict()


@app.get("/unit/")
def get_by_unit(idunidad: int):
        records = controller.get_by_unit(MaintenanceOut,idunidad)
        if not records:
            logger.warning(f"[GET /{idunidad}] Mantenimiento con ID {idunidad} no encontrado.")
            raise HTTPException(status_code=404, detail="Not found")
        
        logger.info(f"[GET /{idunidad}] Se ha encontrado el mantenimiento con ID {idunidad}.")
        return records.to_dict()
@app.get("/listar")
async def listar_mantenimientos(request: Request):
    """
    Muestra la lista de registros de mantenimiento en formato HTML.
    """
    try:
        # Obtener todos los registros de mantenimiento de la base de datos
        mantenimientos = controller.read_all(MaintenanceOut)

        # Renderizar la plantilla HTML con los datos obtenidos
        return mantenimientos
    except Exception as e:
        logger.error(f"[GET /listar] Error al listar mantenimientos: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al listar mantenimientos: {str(e)}")
