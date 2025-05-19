import logging
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.rutaparada import RutaParada

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/ruta_parada", tags=["ruta_parada"])
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_rutaparada(request: Request):
    """
    Lista todas las relaciones Ruta-Parada.
    """
    try:
        rutaparadas = controller.get_ruta_parada()
        logger.info(f"[GET /ruta_parada/] Se listaron {len(rutaparadas)} relaciones Ruta-Parada.")
        return templates.TemplateResponse("ListarRutaParada.html", {"request": request, "rutaparadas": rutaparadas})
    except Exception as e:
        logger.error(f"[GET /ruta_parada/] Error al listar las relaciones Ruta-Parada: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al listar las relaciones Ruta-Parada: {str(e)}")

@app.get("/{id_parada}", response_class=HTMLResponse)
def detalle_rutaparada(id_parada: int, request: Request):
    """
    Obtiene el detalle de una relación Ruta-Parada por su IDParada.
    """
    try:
        resultados = controller.get_ruta_parada(id_parada=id_parada)
        if not resultados:
            logger.warning(f"[GET /ruta_parada/{id_parada}] No se encontraron registros para la parada especificada.")
            raise HTTPException(status_code=404, detail="No se encontraron registros para la parada especificada.")
        logger.info(f"[GET /ruta_parada/{id_parada}] Se consultaron {len(resultados)} registros para la parada.")
        return templates.TemplateResponse("DetalleRutaParada.html", {"request": request, "rutaparadas": resultados})
    except Exception as e:
        logger.error(f"[GET /ruta_parada/{id_parada}] Error al obtener el detalle de la relación Ruta-Parada: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al obtener el detalle de la relación Ruta-Parada: {str(e)}")

@app.get("/filtrar/")
def filtrar_ruta_parada(id_ruta: int = Query(None), id_parada: int = Query(None)):
    """
    Filtra las relaciones Ruta-Parada según el ID de Ruta o ID de Parada.
    """
    try:
        resultados = controller.get_ruta_parada(id_ruta=id_ruta, id_parada=id_parada)
        if not resultados:
            logger.warning(f"[GET /ruta_parada/filtrar/] No se encontraron registros para los filtros dados.")
            raise HTTPException(status_code=404, detail="No se encontraron registros.")
        logger.info(f"[GET /ruta_parada/filtrar/] Se encontraron {len(resultados)} registros para los filtros dados.")
        return resultados
    except Exception as e:
        logger.error(f"[GET /ruta_parada/filtrar/] Error al filtrar las relaciones Ruta-Parada: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error al filtrar las relaciones Ruta-Parada: {str(e)}")