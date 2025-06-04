import logging
import re
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.transport import UnidadTransporte
from backend.app.core.auth import get_current_user
from fastapi import Security

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/transport_units", tags=["transport_units"])

@app.get("/", response_class=JSONResponse)
def listar_unidades_transporte(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operario"])
):
    try:
        unidades = controller.read_all(UnidadTransporte)
        logger.info("[GET /transport_units/] Unidades de transporte listadas.")
        unidades_json = [
            u.model_dump() if hasattr(u, "model_dump")
            else u.dict() if hasattr(u, "dict")
            else u
            for u in unidades
        ]
        return unidades_json
    except Exception as e:
        logger.error("[GET /transport_units/] Error al listar unidades de transporte: %s", e)
        return JSONResponse(
            status_code=500,
            content={"detail": "Error al listar unidades de transporte."}
        )
@app.get("/with_names", response_class=JSONResponse)
def listar_unidades_con_nombres(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operario"])
):
    """
    Lista todas las unidades de transporte mostrando los nombres de ruta y tipo de transporte.
    """
    try:
        unidades = controller.get_all_units_with_names()
        logger.info("[GET /transport_units/with_names] Unidades de transporte con nombres listadas.")
        return unidades
    except Exception as e:
        logger.error("[GET /transport_units/with_names] Error: %s", e)
        return JSONResponse(
            status_code=500,
            content={"detail": "Error al listar unidades de transporte con nombres."}
        )

@app.get("/with_schedules", response_class=JSONResponse)
def listar_unidades_con_horarios(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operario"])
):
    """
    Lista todas las unidades de transporte con sus horarios asociados (por IDRuta).
    """
    try:
        unidades = controller.get_all_units_with_schedules()
        logger.info("[GET /transport_units/with_schedules] Unidades de transporte con horarios listadas.")
        return unidades
    except Exception as e:
        logger.error("[GET /transport_units/with_schedules] Error: %s", e)
        return JSONResponse(
            status_code=500,
            content={"detail": "Error al listar unidades de transporte con horarios."}
        )
@app.get("/{ID}", response_class=JSONResponse)
def detalle_unidad_transporte(
    ID: str,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operario"])
):
    safe_id = re.sub(r"[^\w\-]", "_", ID)
    try:
        unidad = controller.get_by_id(UnidadTransporte, safe_id)
        if not unidad:
            logger.warning("[GET /transport_units/{ID}] Unidad de transporte no encontrada: ID=%s", safe_id)
            return JSONResponse(
                status_code=404,
                content={"detail": "No se encontró la unidad de transporte especificada."}
            )
        logger.info("[GET /transport_units/{ID}] Detalle de unidad de transporte consultado: ID=%s", safe_id)
        if hasattr(unidad, "model_dump"):
            return JSONResponse(status_code=200, content={"data": unidad.model_dump()})
        elif hasattr(unidad, "dict"):
            return JSONResponse(status_code=200, content={"data": unidad.dict()})
        else:
            return JSONResponse(status_code=200, content={"data": unidad})
    except Exception as e:
        logger.error("[GET /transport_units/{ID}] Error al consultar detalle de unidad de transporte: %s", e)
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno al consultar detalle de unidad de transporte."}
        )

