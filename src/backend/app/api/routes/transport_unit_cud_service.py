import logging
from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.transport import UnidadTransporte
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

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
        controller.create(unidad)
        logger.info("[POST /transport_units/create] Unidad de transporte creada exitosamente.")
        return {"message": "Unidad de transporte creada exitosamente."}
    except Exception:
        logger.error("[POST /transport_units/create] Error al crear unidad de transporte.")
        raise HTTPException(status_code=500, detail="Error al crear unidad de transporte.")

@app.post("/update")
def actualizar_unidad_transporte(
    ID: str = Form(...),
    Ubicacion: str = Form(...),
    Capacidad: int = Form(...),
    IDRuta: int = Form(...),
    IDTipo: int = Form(...),
):
    try:
        unidad = UnidadTransporte(ID=ID, Ubicacion=Ubicacion, Capacidad=Capacidad, IDRuta=IDRuta, IDTipo=IDTipo)
        controller.update(unidad)
        logger.info("[POST /transport_units/update] Unidad de transporte actualizada exitosamente.")
        return {"message": "Unidad de transporte actualizada exitosamente."}
    except Exception:
        logger.error("[POST /transport_units/update] Error al actualizar unidad de transporte.")
        raise HTTPException(status_code=500, detail="Error al actualizar unidad de transporte.")

@app.post("/delete")
def eliminar_unidad_transporte(
    ID: str = Form(...),
):
    try:
        controller.delete(UnidadTransporte, ID)
        logger.info("[POST /transport_units/delete] Unidad de transporte eliminada exitosamente.")
        return {"message": "Unidad de transporte eliminada exitosamente."}
    except Exception:
        logger.error("[POST /transport_units/delete] Error al eliminar unidad de transporte.")
        raise HTTPException(status_code=500, detail="Error al eliminar unidad de transporte.")
