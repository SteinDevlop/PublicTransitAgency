import logging
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse
from backend.app.models.rutaparada import RutaParada
from backend.app.logic.universal_controller_instance import universal_controller as controller

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
    IDRuta: int = Form(...)
):
    try:
        existentes = controller.get_ruta_parada(id_ruta=IDRuta, id_parada=IDParada)
        if existentes:
            logger.warning(f"[POST /rutaparada/create] Relación ya existe: IDParada={IDParada}, IDRuta={IDRuta}")
            raise HTTPException(status_code=409, detail="La relación Ruta-Parada ya existe.")
        rutaparada = RutaParada(IDParada=IDParada, IDRuta=IDRuta)
        controller.add(rutaparada)
        logger.info(f"[POST /rutaparada/create] Relación creada: IDParada={IDParada}, IDRuta={IDRuta}")
        return JSONResponse(content={"message": "Relación Ruta-Parada creada exitosamente.", "data": rutaparada.model_dump()})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[POST /rutaparada/create] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update", response_class=JSONResponse)
def actualizar_rutaparada(
    IDParada: int = Form(...),
    IDRuta: int = Form(...),
    nuevo_IDParada: int = Form(None),
    nuevo_IDRuta: int = Form(None)
):
    try:
        existentes = controller.get_ruta_parada(id_ruta=IDRuta, id_parada=IDParada)
        if not existentes:
            logger.warning(f"[POST /rutaparada/update] Relación no encontrada: IDParada={IDParada}, IDRuta={IDRuta}")
            raise HTTPException(status_code=404, detail="Relación Ruta-Parada no encontrada.")
        # Usa el método específico para actualizar
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
        return JSONResponse(content={"message": "Relación Ruta-Parada actualizada exitosamente.", "data": rutaparada_actualizada.model_dump()})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[POST /rutaparada/update] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/delete", response_class=JSONResponse)
def eliminar_rutaparada(
    IDParada: int = Form(...),
    IDRuta: int = Form(...)
):
    try:
        existentes = controller.get_ruta_parada(id_ruta=IDRuta, id_parada=IDParada)
        if not existentes:
            logger.warning(f"[POST /rutaparada/delete] Relación no encontrada: IDParada={IDParada}, IDRuta={IDRuta}")
            raise HTTPException(status_code=404, detail="Relación Ruta-Parada no encontrada.")
        ok = controller.delete_ruta_parada(id_ruta=IDRuta, id_parada=IDParada)
        if not ok:
            raise Exception("No se pudo eliminar la relación.")
        logger.info(f"[POST /rutaparada/delete] Relación eliminada: IDParada={IDParada}, IDRuta={IDRuta}")
        return JSONResponse(content={"message": "Relación Ruta-Parada eliminada exitosamente."})
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[POST /rutaparada/delete] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))