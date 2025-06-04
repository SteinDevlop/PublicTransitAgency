import logging
from fastapi import APIRouter, Form, HTTPException, Security
from fastapi.responses import JSONResponse
from backend.app.models.rutaparada import RutaParada
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(
    prefix="/rutaparada",
    tags=["rutaparada"],
    default_response_class=JSONResponse
)

@app.post("/create", response_class=JSONResponse)
def crear_rutaparada(
    IDParada: int = Form(...),
    IDRuta: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existentes = controller.get_ruta_parada(id_ruta=IDRuta, id_parada=IDParada)
        if existentes:
            logger.warning(f"[POST /rutaparada/create] Relación ya existe: IDParada={IDParada}, IDRuta={IDRuta}")
            return JSONResponse(
                status_code=409,
                content={"detail": "La relación Ruta-Parada ya existe."}
            )
        rutaparada = RutaParada(IDParada=IDParada, IDRuta=IDRuta)
        controller.add(rutaparada)
        logger.info(f"[POST /rutaparada/create] Relación creada: IDParada={IDParada}, IDRuta={IDRuta}")
        return JSONResponse(
            content={"message": "Relación Ruta-Parada creada exitosamente.", "data": rutaparada.model_dump()}
        )
    except Exception as e:
        logger.error(f"[POST /rutaparada/create] Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error interno al crear la relación Ruta-Parada: {str(e)}"}
        )

@app.post("/update", response_class=JSONResponse)
def actualizar_rutaparada(
    IDParada: int = Form(...),
    IDRuta: int = Form(...),
    nuevo_IDParada: int = Form(None),
    nuevo_IDRuta: int = Form(None),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existentes = controller.get_ruta_parada(id_ruta=IDRuta, id_parada=IDParada)
        if not existentes:
            logger.warning(f"[POST /rutaparada/update] Relación no encontrada: IDParada={IDParada}, IDRuta={IDRuta}")
            return JSONResponse(
                status_code=404,
                content={"detail": "Relación Ruta-Parada no encontrada."}
            )
        ok = controller.update_ruta_parada(
            id_ruta=IDRuta,
            id_parada=IDParada,
            nuevo_id_ruta=nuevo_IDRuta if nuevo_IDRuta is not None else IDRuta,
            nuevo_id_parada=nuevo_IDParada if nuevo_IDParada is not None else IDParada
        )
        if not ok:
            raise Exception("No se pudo actualizar la relación.")
        rutaparada_actualizada = RutaParada(
            IDParada=nuevo_IDParada if nuevo_IDParada is not None else IDParada,
            IDRuta=nuevo_IDRuta if nuevo_IDRuta is not None else IDRuta
        )
        logger.info(f"[POST /rutaparada/update] Relación actualizada: {IDParada},{IDRuta} -> {rutaparada_actualizada.IDParada},{rutaparada_actualizada.IDRuta}")
        return JSONResponse(
            content={"message": "Relación Ruta-Parada actualizada exitosamente.", "data": rutaparada_actualizada.model_dump()}
        )
    except Exception as e:
        logger.error(f"[POST /rutaparada/update] Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error interno al actualizar la relación Ruta-Parada: {str(e)}"}
        )

@app.post("/delete", response_class=JSONResponse)
def eliminar_rutaparada(
    IDParada: int = Form(...),
    IDRuta: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existentes = controller.get_ruta_parada(id_ruta=IDRuta, id_parada=IDParada)
        if not existentes:
            logger.warning(f"[POST /rutaparada/delete] Relación no encontrada: IDParada={IDParada}, IDRuta={IDRuta}")
            return JSONResponse(
                status_code=404,
                content={"detail": "Relación Ruta-Parada no encontrada."}
            )
        ok = controller.delete_ruta_parada(id_ruta=IDRuta, id_parada=IDParada)
        if not ok:
            raise Exception("No se pudo eliminar la relación.")
        logger.info(f"[POST /rutaparada/delete] Relación eliminada: IDParada={IDParada}, IDRuta={IDRuta}")
        return JSONResponse(
            content={"message": "Relación Ruta-Parada eliminada exitosamente."}
        )
    except Exception as e:
        logger.error(f"[POST /rutaparada/delete] Error: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Error interno al eliminar la relación Ruta-Parada: {str(e)}"}
        )