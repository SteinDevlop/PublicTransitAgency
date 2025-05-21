from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.transport import UnidadTransporte
from backend.app.core.auth import get_current_user

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from fastapi import APIRouter

app = APIRouter()

@app.post("/transport_units/create")
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
        logger.info("[POST /transport_units/create] Unidad de transporte creada exitosamente.")
        return {"message": "Unidad de transporte creada exitosamente."}
    except Exception as e:
        logger.error(f"[POST /transport_units/create] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transport_units/update")
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
            logger.warning(f"[POST /transport_units/update] Unidad de transporte no encontrada: ID={ID}")
            raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada.")
        unidad = UnidadTransporte(ID=ID, Ubicacion=Ubicacion, Capacidad=Capacidad, IDRuta=IDRuta, IDTipo=IDTipo)
        controller.update(unidad)
        logger.info(f"[POST /transport_units/update] Unidad de transporte actualizada exitosamente: ID={ID}")
        return {"message": "Unidad de transporte actualizada exitosamente."}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[POST /transport_units/update] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/transport_units/delete")
def eliminar_unidad_transporte(
    ID: str = Form(...),
):
    try:
        existing = controller.get_by_id(UnidadTransporte, ID)
        if not existing:
            logger.warning(f"[POST /transport_units/delete] Unidad de transporte no encontrada: ID={ID}")
            raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada.")
        controller.delete(existing)
        logger.info(f"[POST /transport_units/delete] Unidad de transporte eliminada exitosamente: ID={ID}")
        return {"message": "Unidad de transporte eliminada exitosamente."}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[POST /transport_units/delete] Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))