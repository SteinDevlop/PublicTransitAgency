import logging
from fastapi import APIRouter, Form, Request, HTTPException, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from backend.app.models.maintainance import MaintenanceCreate, MaintenanceOut
from backend.app.logic.universal_controller_postgres import UniversalController
from backend.app.core.auth import get_current_user

# Initialize the controller and templates
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Define the APIRouter with a prefix and tags
app = APIRouter(prefix="/maintainance", tags=["maintainance"])

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@app.get("/maintenance/token_info", response_model=dict[str, str])
async def maintenance_token_info(request: Request, token_info= get_current_user):
    return {"token_info": token_info}

@app.get("/crear", response_class=HTMLResponse)
def crear_mantenimiento(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor", "tecnico", "operador"])
):
    """
    Route to display the maintenance creation form.
    """
    logger.info(f"[GET /crear] Usuario {current_user['user_id']} accede al formulario para crear mantenimiento.")
    return templates.TemplateResponse(request,"CrearMantenimiento.html", {"request": request})


@app.get("/eliminar", response_class=HTMLResponse)
def eliminar_mantenimiento(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "tecnico"])
):
    """
    Route to display the maintenance deletion form.
    """
    logger.info(f"[GET /eliminar] Usuario {current_user['user_id']} accede al formulario para eliminar mantenimiento.")
    return templates.TemplateResponse(request,"EliminarMantenimiento.html", {"request": request})


@app.get("/actualizar", response_class=HTMLResponse)
def actualizar_mantenimiento(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "tecnico"])
):
    """
    Route to display the maintenance update form.
    """
    logger.info(f"[GET /actualizar] Usuario {current_user['user_id']} accede al formulario para actualizar mantenimiento.")
    return templates.TemplateResponse(request,"ActualizarMantenimiento.html", {"request": request})


@app.post("/create")
async def add(
    id: int = Form(...),
    idestado: int = Form(...),
    tipo: str = Form(...),
    fecha: datetime = Form(...),
    idunidadtransporte: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "tecnico"])
):
    """
    Route to add a new maintenance record.
    Receives maintenance information and creates a MaintenanceCreate object.
    """
    logger.info(f"[POST /create] Usuario {current_user['user_id']} intenta crear mantenimiento: {id}, {idestado}, {tipo}, {fecha}, {idunidadtransporte}.")
    
    maintenance_temp = MaintenanceCreate(
        id=id,
        idestado=idestado,
        tipo=tipo,
        fecha=fecha,
        idunidadtransporte=idunidadtransporte
    )
    
    try:
        controller.add(maintenance_temp)
        logger.info(f"[POST /create] Mantenimiento con ID {maintenance_temp.idunidadtransporte} creado con éxito.")
        return {"message": "Maintenance added successfully"}
    except Exception as e:
        logger.error(f"[POST /create] Error al crear mantenimiento: {e}")
        raise HTTPException(status_code=500, detail=str(e))  # Handle any exceptions


@app.post("/update")
async def update(
    id: int = Form(...),
    idestado: int = Form(...),
    tipo: str = Form(...),
    fecha: datetime = Form(...),
    idunidadtransporte: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "tecnico"])
):
    """
    Route to update an existing maintenance record.
    Checks if the maintenance record exists and updates it with new data.
    """
    logger.info(f"[POST /update] Usuario {current_user['user_id']} intenta actualizar mantenimiento con ID {id}.")
    
    existing_maintenance = controller.get_by_id(MaintenanceOut, id)
    
    if not existing_maintenance:
        logger.warning(f"[POST /update] No se encontró mantenimiento con ID {id}.")
        raise HTTPException(status_code=404, detail="Maintenance not found")
    
    maintenance_temp = MaintenanceCreate(
        id=id,  # The ID must remain the same to update the object
        idestado=idestado,
        tipo=tipo,
        fecha=fecha,
        idunidadtransporte=idunidadtransporte
    )
    
    try:
        controller.update(maintenance_temp)
        logger.info(f"[POST /update] Mantenimiento con ID {id} actualizado con éxito.")
        return {"message": f"Maintenance {id} updated successfully"}
    except Exception as e:
        logger.error(f"[POST /update] Error al actualizar mantenimiento: {e}")
        raise HTTPException(status_code=500, detail=str(e))  # Handle any exceptions


@app.post("/delete")
async def delete_maintenance(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "tecnico"])
):
    """
    Route to delete an existing maintenance record by its ID.
    """
    logger.info(f"[POST /delete] Usuario {current_user['user_id']} intenta eliminar mantenimiento con ID {id}.")
    
    try:
        existing_maintenance = controller.get_by_id(MaintenanceOut, id)
        if not existing_maintenance:
            logger.warning(f"[POST /delete] No se encontró mantenimiento con ID {id}.")
            raise HTTPException(status_code=404, detail="Maintenance not found")
        
        controller.delete(existing_maintenance)
        logger.info(f"[POST /delete] Mantenimiento con ID {id} eliminado con éxito.")
        return {"message": f"Maintenance {id} deleted successfully"}
    except HTTPException:
        raise  # Re-raises HTTPException as is
    except Exception as e:
        logger.error(f"[POST /delete] Error al eliminar mantenimiento: {e}")
        raise HTTPException(status_code=500, detail=str(e))  # Internal server error for other exceptions
