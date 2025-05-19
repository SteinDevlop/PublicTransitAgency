import logging
from fastapi import APIRouter, Form, HTTPException, Security

from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.incidence import Incidence
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/incidences", tags=["incidences"])

@app.post("/create")
def crear_incidencia(
    ID : int = Form(...),
    IDTicket: int = Form(...),
    Descripcion: str = Form(...),
    Tipo: str = Form(...),
    IDUnidad: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Crea una nueva incidencia.
    """
    incidencia = Incidence(ID=ID, IDTicket=IDTicket, Descripcion=Descripcion, Tipo=Tipo, IDUnidad=IDUnidad)
    try:
        controller.add(incidencia)
        logger.info(f"[POST /incidences/create] Incidencia creada exitosamente: {incidencia}")
        return {"message": "Incidencia creada exitosamente.", "data": incidencia.to_dict()}
    except ValueError as e:
        logger.warning(f"[POST /incidences/create] Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_incidencia(
    ID: int = Form(...),
    IDTicket: int = Form(...),
    Descripcion: str = Form(...),
    Tipo: str = Form(...),
    IDUnidad: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Actualiza una incidencia existente.
    """
    incidencia_actualizada = Incidence(ID=ID, IDTicket=IDTicket, Descripcion=Descripcion, Tipo=Tipo, IDUnidad=IDUnidad)
    try:
        controller.update(incidencia_actualizada)
        logger.info(f"[POST /incidences/update] Incidencia actualizada exitosamente: {incidencia_actualizada}")
        return {"message": "Incidencia actualizada exitosamente.", "data": incidencia_actualizada.to_dict()}
    except ValueError as e:
        logger.warning(f"[POST /incidences/update] Error de validación: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_incidencia(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Elimina una incidencia por su ID.
    """
    existing_incidencia = controller.get_by_id(Incidence, ID)
    if not existing_incidencia:
        logger.warning(f"[POST /incidences/delete] Incidencia no encontrada: ID={ID}")
        raise HTTPException(status_code=404, detail="Incidencia no encontrada.")

    try:
        controller.delete(existing_incidencia)
        logger.info(f"[POST /incidences/delete] Incidencia eliminada exitosamente: ID={ID}")
        return {"message": "Incidencia eliminada exitosamente."}
    except ValueError as e:
        logger.warning(f"[POST /incidences/delete] Error al eliminar: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))