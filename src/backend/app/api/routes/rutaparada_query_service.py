import logging
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/ruta_parada", tags=["ruta_parada"])

@app.get("/", response_class=JSONResponse)
def listar_rutaparada():
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

@app.get("/{id_parada}", response_class=JSONResponse)
def detalle_rutaparada(id_parada: int):
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

@app.get("/filtrar/", response_class=JSONResponse)
def filtrar_ruta_parada(id_ruta: int = Query(None), id_parada: int = Query(None)):
    """
    Filtra las relaciones Ruta-Parada según el ID de Ruta o ID de Parada.
    """
    try:
        # Se pasan explícitamente los argumentos id_ruta y id_parada
        resultados = controller.get_ruta_parada(id_ruta=id_ruta, id_parada=id_parada)
        if not resultados:
            logger.warning(f"[GET /ruta_parada/filtrar/] No se encontraron registros para los filtros especificados.")
            return JSONResponse(
                status_code=404,
                content={"detail": "No se encontraron registros para los filtros especificados."}
            )
        logger.info(f"[GET /ruta_parada/filtrar/] Se consultaron {len(resultados)} registros con los filtros especificados.")
        return {"data": resultados}
    except Exception as e:
        logger.error(f"[GET /ruta_parada/filtrar/] Error al filtrar las relaciones Ruta-Parada: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Error interno al filtrar las relaciones Ruta-Parada."}
        )