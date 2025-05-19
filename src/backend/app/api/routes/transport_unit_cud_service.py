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
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Crea una nueva unidad de transporte.
    """
    unidad = UnidadTransporte(Ubicacion=Ubicacion, Capacidad=Capacidad, IDRuta=IDRuta, IDTipo=IDTipo, ID=ID)
    try:
        controller.add(unidad)
        logger.info(f"[POST /transport_units/create] Unidad de transporte creada exitosamente: {unidad}")
        return {"message": "Unidad de transporte creada exitosamente.", "data": unidad.to_dict()}
    except ValueError as e:
        logger.warning(f"[POST /transport_units/create] Error al crear la unidad: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_unidad_transporte(
    ID: str = Form(...),
    Ubicacion: str = Form(...),
    Capacidad: int = Form(...),
    IDRuta: int = Form(...),
    IDTipo: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Actualiza una unidad de transporte existente.
    """
    existing_unidad = controller.get_by_id(UnidadTransporte, ID)
    if not existing_unidad:
        logger.warning(f"[POST /transport_units/update] Unidad de transporte no encontrada: ID={ID}")
        raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada.")

    unidad_actualizada = UnidadTransporte(Ubicacion=Ubicacion, Capacidad=Capacidad, IDRuta=IDRuta, IDTipo=IDTipo, ID=ID)
    try:
        controller.update(unidad_actualizada)
        logger.info(f"[POST /transport_units/update] Unidad de transporte actualizada exitosamente: {unidad_actualizada}")
        return {"message": "Unidad de transporte actualizada exitosamente.", "data": unidad_actualizada.to_dict()}
    except ValueError as e:
        logger.warning(f"[POST /transport_units/update] Error al actualizar la unidad: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_unidad_transporte(
    ID: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor"])
):
    """
    Elimina una unidad de transporte por su ID.
    """
    existing_unidad = controller.get_by_id(UnidadTransporte, ID)
    if not existing_unidad:
        logger.warning(f"[POST /transport_units/delete] Unidad de transporte no encontrada: ID={ID}")
        raise HTTPException(status_code=404, detail="Unidad de transporte no encontrada.")

    try:
        controller.delete(existing_unidad)
        logger.info(f"[POST /transport_units/delete] Unidad de transporte eliminada exitosamente: ID={ID}")
        return {"message": "Unidad de transporte eliminada exitosamente."}
    except ValueError as e:
        logger.warning(f"[POST /transport_units/delete] Error al eliminar la unidad: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))