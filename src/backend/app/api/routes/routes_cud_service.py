import logging
from fastapi import APIRouter, Form, HTTPException, Security
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.routes import Ruta
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/routes", tags=["routes"])

@app.post("/create")
def crear_ruta(
    ID: int = Form(...),
    IDHorario: int = Form(...),
    Nombre: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Crea una nueva ruta.
    """
    ruta = Ruta(ID=ID, IDHorario=IDHorario, Nombre=Nombre)
    try:
        controller.add(ruta)
        logger.info(f"[POST /routes/create] Ruta creada exitosamente: {ruta}")
        return {"message": "Ruta creada exitosamente.", "data": ruta.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /routes/create] Error al crear la ruta: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error al crear la ruta: {str(e)}")

@app.post("/update")
def actualizar_ruta(
    ID: int = Form(...),
    IDHorario: int = Form(...),
    Nombre: str = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Actualiza una ruta existente.
    """
    existing_route = controller.get_by_id(Ruta, ID)
    if not existing_route:
        logger.warning(f"[POST /routes/update] Ruta no encontrada: ID={ID}")
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    ruta_actualizada = Ruta(ID=ID, IDHorario=IDHorario, Nombre=Nombre)
    try:
        controller.update(ruta_actualizada)
        logger.info(f"[POST /routes/update] Ruta actualizada exitosamente: {ruta_actualizada}")
        return {"message": "Ruta actualizada exitosamente.", "data": ruta_actualizada.to_dict()}
    except Exception as e:
        logger.warning(f"[POST /routes/update] Error al actualizar la ruta: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error al actualizar la ruta: {str(e)}")

@app.post("/delete")
def eliminar_ruta(
    ID: int = Form(...),
    #current_user: dict = Security(get_current_user, scopes=["system", "administrador", "planificador"])
):
    """
    Elimina una ruta por su ID.
    """
    existing_route = controller.get_by_id(Ruta, ID)
    if not existing_route:
        logger.warning(f"[POST /routes/delete] Ruta no encontrada: ID={ID}")
        raise HTTPException(status_code=404, detail="Ruta no encontrada")

    try:
        controller.delete(existing_route)
        logger.info(f"[POST /routes/delete] Ruta eliminada exitosamente: ID={ID}")
        return {"message": "Ruta eliminada exitosamente."}
    except Exception as e:
        logger.warning(f"[POST /routes/delete] Error al eliminar la ruta: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error al eliminar la ruta: {str(e)}")