import logging
from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.shift import Shift
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/shifts", tags=["shifts"])

@app.post("/create")
def crear_turno(
    id: int = Form(...),
    TipoTurno: str = Form(...),
   #current_user: dict  = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Crea un turno con los datos proporcionados.
    """
    turno = Shift(ID=id, TipoTurno=TipoTurno)
    try:
        controller.add(turno)
        logger.info(f"[POST /shifts/create] Turno creado exitosamente: {turno}")
        return {"message": "Turno creado exitosamente.", "data": turno.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /shifts/create] Error al crear el turno: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_turno(
    id: int = Form(...),
    TipoTurno: str = Form(...),
   #current_user: dict  = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Actualiza la información de un turno existente.
    """
    existing_turno = controller.get_by_id(Shift, id)
    if not existing_turno:
        logger.warning(f"[POST /shifts/update] Turno no encontrado: ID={id}")
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    turno_actualizado = Shift(ID=id, TipoTurno=TipoTurno)
    try:
        controller.update(turno_actualizado)
        logger.info(f"[POST /shifts/update] Turno actualizado exitosamente: {turno_actualizado}")
        return {"message": "Turno actualizado exitosamente.", "data": turno_actualizado.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /shifts/update] Error al actualizar el turno: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_turno(
    id: int = Form(...),
   #current_user: dict  = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Elimina un turno existente por su ID.
    """
    existing_turno = controller.get_by_id(Shift, id)
    if not existing_turno:
        logger.warning(f"[POST /shifts/delete] Turno no encontrado: ID={id}")
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    try:
        controller.delete(existing_turno)
        logger.info(f"[POST /shifts/delete] Turno eliminado exitosamente: ID={id}")
        return {"message": "Turno eliminado exitosamente."}
    except Exception as e:
        logger.warning(f"[POST /shifts/delete] Error al eliminar el turno: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))