import logging
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.rutaparada import RutaParada

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/ruta_parada", tags=["ruta_parada"])

@app.get("/", response_class=JSONResponse)
def listar_rutaparada():
    """
    Lista todas las relaciones Ruta-Parada.
    """
    try:
        rutaparadas = controller.get_ruta_parada()
        logger.info(f"[GET /ruta_parada/] Se listaron {len(rutaparadas)} relaciones Ruta-Parada.")
        rutaparadas_json = [
            r.model_dump() if hasattr(r, "model_dump")
            else r.dict() if hasattr(r, "dict")
            else r
            for r in rutaparadas
        ]
        return rutaparadas_json
    except Exception as e:
        logger.error(f"[GET /ruta_parada/] Error al listar las relaciones Ruta-Parada: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al listar las relaciones Ruta-Parada: {str(e)}")

@app.get("/{id_parada}", response_class=JSONResponse)
def detalle_rutaparada(id_parada: int):
    """
    Obtiene el detalle de una relación Ruta-Parada por su IDParada.
    """
    try:
        resultados = controller.get_ruta_parada(id_parada=id_parada)
        if not resultados:
            logger.warning(f"[GET /ruta_parada/{id_parada}] No se encontraron registros para la parada especificada.")
            raise HTTPException(status_code=404, detail="No se encontraron registros para la parada especificada.")
        logger.info(f"[GET /ruta_parada/{id_parada}] Se consultaron {len(resultados)} registros para la parada.")
        resultados_json = [
            r.model_dump() if hasattr(r, "model_dump")
            else r.dict() if hasattr(r, "dict")
            else r
            for r in resultados
        ]
        return resultados_json
    except Exception as e:
        logger.error(f"[GET /ruta_parada/{id_parada}] Error al obtener el detalle de la relación Ruta-Parada: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener el detalle de la relación Ruta-Parada: {str(e)}")