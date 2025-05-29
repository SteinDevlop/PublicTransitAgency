import logging
from fastapi import APIRouter, Form, HTTPException, Security
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.schedule import Schedule
# from backend.app.core.auth import get_current_user  # Comentado para inutilizar autenticación temporalmente
# from backend.app.core.conf import headers  # Comentado para inutilizar autenticación temporalmente

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

HORARIO_NO_ENCONTRADO = "Horario no encontrado."
ERROR_AL_CREAR = "Error al crear el horario."
ERROR_AL_ACTUALIZAR = "Error al actualizar el horario."
ERROR_AL_ELIMINAR = "Error al eliminar el horario."

app = APIRouter(prefix="/schedules", tags=["schedules"])

@app.post("/create")
def crear_horario(
    ID: int = Form(...),
    Llegada: str = Form(...),
    Salida: str = Form(...),
    # current_user: dict = Security(get_current_user, scopes=["system"])  # Comentado para inutilizar autenticación temporalmente
):
    """
    Crea un nuevo horario.
    """
    new_schedule = Schedule(ID=ID, Llegada=Llegada, Salida=Salida)
    try:
        controller.add(new_schedule)
        logger.info(f"[POST /schedules/create] Horario creado exitosamente: {new_schedule}")
        return {"message": "Horario creado exitosamente.", "data": new_schedule.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /schedules/create] {ERROR_AL_CREAR}: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"detail": ERROR_AL_CREAR}
        )

@app.post("/update")
def actualizar_horario(
    ID: int = Form(...),
    Llegada: str = Form(...),
    Salida: str = Form(...),
    # current_user: dict = Security(get_current_user, scopes=["system"])  # Comentado para inutilizar autenticación temporalmente
):
    updated_schedule = Schedule(ID=ID, Llegada=Llegada, Salida=Salida)
    try:
        controller.update(updated_schedule)
        logger.info(f"[POST /schedules/update] Horario actualizado exitosamente: {updated_schedule}")
        return {"message": "Horario actualizado exitosamente.", "data": updated_schedule.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /schedules/update] {ERROR_AL_ACTUALIZAR}: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"detail": ERROR_AL_ACTUALIZAR}
        )

@app.post("/delete")
def eliminar_horario(
    ID: int = Form(...),
    # current_user: dict = Security(get_current_user, scopes=["system"])  # Comentado para inutilizar autenticación temporalmente
):
    try:
        existing_schedule = controller.get_by_id(Schedule, ID)
        if not existing_schedule:
            logger.warning(f"[POST /schedules/delete] {HORARIO_NO_ENCONTRADO}: ID={ID}")
            return JSONResponse(
                status_code=404,
                content={"detail": HORARIO_NO_ENCONTRADO}
            )
        controller.delete(existing_schedule)
        logger.info(f"[POST /schedules/delete] Horario eliminado exitosamente: ID={ID}")
        return {"message": "Horario eliminado exitosamente."}
    except Exception as e:
        logger.warning(f"[POST /schedules/delete] {ERROR_AL_ELIMINAR}: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={"detail": ERROR_AL_ELIMINAR}
        )