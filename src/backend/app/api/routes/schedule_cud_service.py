import logging
from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.models.schedule import Schedule
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/schedules", tags=["schedules"])

@app.post("/create")
def crear_horario(
    ID: int = Form(...),
    Llegada: str = Form(...),
    Salida: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Endpoint para crear un horario.
    """
    schedule = Schedule(ID=ID, Llegada=Llegada, Salida=Salida)
    try:
        controller.add(schedule)
        logger.info(f"[POST /schedules/create] Horario creado exitosamente: {schedule}")
        return {"message": "Horario creado exitosamente.", "data": schedule.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /schedules/create] Error al crear el horario: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_horario(
    id: int = Form(...),
    Llegada: str = Form(...),
    Salida: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Endpoint para actualizar un horario existente.
    """
    existing_schedule = controller.get_by_id(Schedule, id)
    if not existing_schedule:
        logger.warning(f"[POST /schedules/update] Horario no encontrado: ID={id}")
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    updated_schedule = Schedule(ID=id, Llegada=Llegada, Salida=Salida)
    try:
        controller.update(updated_schedule)
        logger.info(f"[POST /schedules/update] Horario actualizado exitosamente: {updated_schedule}")
        return {"message": "Horario actualizado exitosamente.", "data": updated_schedule.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /schedules/update] Error al actualizar el horario: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_horario(
    id: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Endpoint para eliminar un horario por su ID.
    """
    existing_schedule = controller.get_by_id(Schedule, id)
    if not existing_schedule:
        logger.warning(f"[POST /schedules/delete] Horario no encontrado: ID={id}")
        raise HTTPException(status_code=404, detail="Horario no encontrado")

    try:
        controller.delete(existing_schedule)
        logger.info(f"[POST /schedules/delete] Horario eliminado exitosamente: ID={id}")
        return {"message": "Horario eliminado exitosamente."}
    except Exception as e:
        logger.warning(f"[POST /schedules/delete] Error al eliminar el horario: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))