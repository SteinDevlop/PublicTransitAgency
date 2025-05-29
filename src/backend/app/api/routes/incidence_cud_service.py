import logging
from fastapi import APIRouter, Form, HTTPException, Security

from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.incidence import Incidence
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
glob="Incidencia no encontrada"
app = APIRouter(prefix="/incidences", tags=["incidences"])

@app.post("/create")
def crear_incidencia(
    ID : int = Form(...),
    IDTicket: int = Form(...),
    Descripcion: str = Form(...),
    Tipo: str = Form(...),
    IDUnidad: str = Form(...),
   #current_user: dict  = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
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
):
    try:
        existing_incidencia = controller.get_by_id(Incidence, ID)
    except Exception:
        logger.error(f"[POST /incidences/update] Error al buscar incidencia ID={ID}")
        raise HTTPException(status_code=404, detail="Incidencia no encontrada.")

    if not existing_incidencia:
        logger.warning(f"[POST /incidences/update] {glob}: ID={ID}")
        raise HTTPException(status_code=404, detail=glob)

    try:
        incidencia_actualizada = Incidence(ID=ID, IDTicket=IDTicket, Descripcion=Descripcion, Tipo=Tipo, IDUnidad=IDUnidad)
        controller.update(incidencia_actualizada)
        logger.info(f"[POST /incidences/update] Incidencia actualizada exitosamente: {incidencia_actualizada}")
        return {"message": "Incidencia actualizada exitosamente.", "data": incidencia_actualizada.to_dict()}
    except Exception as e:
        logger.error(f"[POST /incidences/update] Error al actualizar incidencia: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_incidencia(
    ID: int = Form(...),
):
    try:
        existing_incidencia = controller.get_by_id(Incidence, ID)
    except Exception:
        logger.error(f"[POST /incidences/delete] Error al buscar incidencia ID={ID}")
        raise HTTPException(status_code=404, detail="Incidencia no encontrada.")

    if not existing_incidencia:
        logger.warning(f"[POST /incidences/delete] {glob}: ID={ID}")
        raise HTTPException(status_code=404, detail=glob)

    try:
        controller.delete(existing_incidencia)
        logger.info(f"[POST /incidences/delete] Incidencia eliminada exitosamente: ID={ID}")
        return {"message": "Incidencia eliminada exitosamente."}
    except Exception as e:
        logger.error(f"[POST /incidences/delete] Error al eliminar incidencia: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))