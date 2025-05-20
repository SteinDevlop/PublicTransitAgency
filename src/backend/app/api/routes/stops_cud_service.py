import logging
from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.models.stops import Parada
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/stops", tags=["stops"])

@app.post("/create")
def crear_parada(
    id: int = Form(...),
    Nombre: str = Form(...),
    Ubicacion: str = Form(...),
   #current_user: dict  = Security(get_current_user)
):
    """
    Endpoint para crear una parada.
    """
    parada = Parada(ID=id, Nombre=Nombre, Ubicacion=Ubicacion)
    try:
        controller.add(parada)
        logger.info(f"[POST /stops/create] Parada creada exitosamente: {parada}")
        return {"message": "Parada creada exitosamente.", "data": parada.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /stops/create] Error al crear la parada: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/update")
def actualizar_parada(
    id: int = Form(...),
    Nombre: str = Form(...),
    Ubicacion: str = Form(...),
   #current_user: dict  = Security(get_current_user)
):
    """
    Endpoint para actualizar una parada existente.
    """
    existing_parada = controller.get_by_id(Parada, id)
    if not existing_parada:
        logger.warning(f"[POST /stops/update] Parada no encontrada: ID={id}")
        raise HTTPException(status_code=404, detail="Parada no encontrada")

    updated_parada = Parada(ID=id, Nombre=Nombre, Ubicacion=Ubicacion)
    try:
        controller.update(updated_parada)
        logger.info(f"[POST /stops/update] Parada actualizada exitosamente: {updated_parada}")
        return {"message": "Parada actualizada exitosamente.", "data": updated_parada.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /stops/update] Error al actualizar la parada: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/delete")
def eliminar_parada(
    id: int = Form(...),
   #current_user: dict  = Security(get_current_user)
):
    """
    Endpoint para eliminar una parada por su ID.
    """
    existing_parada = controller.get_by_id(Parada, id)
    if not existing_parada:
        logger.warning(f"[POST /stops/delete] Parada no encontrada: ID={id}")
        raise HTTPException(status_code=404, detail="Parada no encontrada")

    try:
        controller.delete(existing_parada)
        logger.info(f"[POST /stops/delete] Parada eliminada exitosamente: ID={id}")
        return {"message": "Parada eliminada exitosamente."}
    except Exception as e:
        logger.warning(f"[POST /stops/delete] Error al eliminar la parada: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))