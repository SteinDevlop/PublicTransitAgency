import logging
from fastapi import APIRouter, Form, Depends, Security
from fastapi.responses import JSONResponse

from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.incidence import Incidence
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

INCIDENCIA_NO_ENCONTRADA = "Incidencia no encontrada."
ERROR_AL_ACTUALIZAR = "Error al actualizar incidencia."
ERROR_AL_ELIMINAR = "Error al eliminar incidencia."

app = APIRouter(prefix="/incidences", tags=["incidences"])

@app.post("/create")
def crear_incidencia(
    ID: int = Form(...),
    IDTicket: int = Form(...),
    Descripcion: str = Form(...),
    Tipo: str = Form(...),
    IDUnidad: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operario"]),
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
        return JSONResponse(
            status_code=400,
            content={"detail": str(e)}
        )

@app.post("/update")
def actualizar_incidencia(
    ID: int = Form(...),
    IDTicket: int = Form(...),
    Descripcion: str = Form(...),
    Tipo: str = Form(...),
    IDUnidad: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operario"]),
):
    try:
        existing_incidencia = controller.get_by_id(Incidence, ID)
        if not existing_incidencia:
            logger.warning(f"[POST /incidences/update] {INCIDENCIA_NO_ENCONTRADA}: ID={ID}")
            return JSONResponse(
                status_code=404,
                content={"detail": INCIDENCIA_NO_ENCONTRADA}
            )
        # Actualización lógica aquí...
        logger.info(f"[POST /incidences/update] Incidencia actualizada: ID={ID}")
        return {"message": "Incidencia actualizada exitosamente."}
    except Exception as e:
        logger.error(f"[POST /incidences/update] {ERROR_AL_ACTUALIZAR}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": ERROR_AL_ACTUALIZAR}
        )

@app.post("/delete")
def eliminar_incidencia(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"]),
):
    try:
        existing_incidencia = controller.get_by_id(Incidence, ID)
        if not existing_incidencia:
            logger.warning(f"[POST /incidences/delete] {INCIDENCIA_NO_ENCONTRADA}: ID={ID}")
            return JSONResponse(
                status_code=404,
                content={"detail": INCIDENCIA_NO_ENCONTRADA}
            )
        controller.delete(existing_incidencia)
        logger.info(f"[POST /incidences/delete] Incidencia eliminada: ID={ID}")
        return {"message": "Incidencia eliminada exitosamente."}
    except Exception as e:
        logger.error(f"[POST /incidences/delete] {ERROR_AL_ELIMINAR}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": ERROR_AL_ELIMINAR}
        )