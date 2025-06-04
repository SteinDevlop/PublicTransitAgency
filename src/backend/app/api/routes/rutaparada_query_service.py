import logging
from fastapi import APIRouter, HTTPException, Query, Security
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/ruta_parada", tags=["ruta_parada"])

@app.get("/", response_class=JSONResponse)
def listar_rutaparada(
):
    """
    Lista todas las relaciones Ruta-Parada.
    """
    try:
        rutaparadas = controller.get_all_rutaparada()
        if not rutaparadas:
            logger.warning("[GET /ruta_parada/] No se encontraron registros.")
            return JSONResponse(
                status_code=404,
                content={"detail": "No se encontraron registros."}
            )
        logger.info(f"[GET /ruta_parada/] Se listaron {len(rutaparadas)} relaciones Ruta-Parada.")
        return {"data": rutaparadas}
    except Exception as e:
        logger.error(f"[GET /ruta_parada/] Error al listar las relaciones Ruta-Parada: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno al listar las relaciones Ruta-Parada."}
        )
@app.get("/solo_nombres", response_class=JSONResponse)
def listar_rutaparada_nombres(
):
    """
    Lista solo los nombres de las rutas y paradas.
    """
    try:
        nombres = controller.get_ruta_parada_nombres()
        if not nombres:
            logger.warning("[GET /ruta_parada/solo_nombres] No se encontraron registros.")
            return JSONResponse(
                status_code=404,
                content={"detail": "No se encontraron registros."}
            )
        logger.info(f"[GET /ruta_parada/solo_nombres] Se listaron {len(nombres)} relaciones Ruta-Parada (solo nombres).")
        return nombres
    except Exception as e:
        logger.error(f"[GET /ruta_parada/solo_nombres] Error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno al listar los nombres de las relaciones Ruta-Parada."}
        )

@app.get("/{id_parada}", response_class=JSONResponse)
def detalle_rutaparada(
    id_parada: int,
):
    """
    Obtiene el detalle de una relación Ruta-Parada por su IDParada.
    """
    try:
        # Se utiliza la función específica del controlador para buscar por IDParada
        resultados = controller.get_by_id_parada(id_parada)
        if not resultados:
            logger.warning(f"[GET /ruta_parada/{id_parada}] No se encontraron registros para la parada especificada.")
            return JSONResponse(
                status_code=404,
                content={"detail": "No se encontraron registros para la parada especificada."}
            )
        logger.info(f"[GET /ruta_parada/{id_parada}] Se consultaron {len(resultados)} registros para la parada.")
        return {"data": resultados}
    except Exception as e:
        logger.error(f"[GET /ruta_parada/{id_parada}] Error al obtener el detalle de la relación Ruta-Parada: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno al obtener el detalle de la relación Ruta-Parada."}
        )

