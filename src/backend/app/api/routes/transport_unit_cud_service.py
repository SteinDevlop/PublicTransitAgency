from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.transport import UnidadTransporte
from backend.app.core.auth import get_current_user

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from fastapi import APIRouter

app = APIRouter(prefix="/transport_units", tags=["transport_units"])

@app.post("/create")
def crear_unidad_transporte(
    Ubicacion: str = Form(...),
    Capacidad: int = Form(...),
    IDRuta: int = Form(...),
    IDTipo: int = Form(...),
    ID: str = Form("EMPTY"),
):
    try:
        unidad = UnidadTransporte(Ubicacion=Ubicacion, Capacidad=Capacidad, IDRuta=IDRuta, IDTipo=IDTipo, ID=ID)
        controller.add(unidad)
        logger.info("[POST /create] Unidad de transporte creada exitosamente.")
        return {"message": "Unidad de transporte creada exitosamente."}
    except Exception as e:
        logger.error(f"[POST /create] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/update")
def actualizar_unidad_transporte(
    ID: str = Form(...),
    Ubicacion: str = Form(...),
    Capacidad: int = Form(...),
    IDRuta: int = Form(...),
    IDTipo: int = Form(...),
):
    try:
        existing = controller.get_by_id(UnidadTransporte, ID)
        if not existing:
            logger.warning("[POST /update] Unidad de transporte no encontrada: ID=%r", ID)
            raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada.")
        unidad = UnidadTransporte(ID=ID, Ubicacion=Ubicacion, Capacidad=Capacidad, IDRuta=IDRuta, IDTipo=IDTipo)
        controller.update(unidad)
        logger.info(f"[POST /update] Unidad de transporte actualizada exitosamente: ID={ID}")
        return {"message": "Unidad de transporte actualizada exitosamente."}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[POST /update] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/delete")
def eliminar_unidad_transporte(
    ID: str = Form(...),
):
    try:
        existing = controller.get_by_id(UnidadTransporte, ID)
        if not existing:
            # Evita inyección en logs usando parámetros separados
            logger.warning("[POST /delete] Unidad de transporte no encontrada: ID=%r", ID)
            raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada.")
        controller.delete(existing)
        logger.info("[POST /delete] Unidad de transporte eliminada exitosamente: ID=%r", ID)
        return {"message": "Unidad de transporte eliminada exitosamente."}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("[POST /delete] Error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))