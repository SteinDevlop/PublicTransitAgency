import logging
from fastapi import (
    Form, HTTPException, APIRouter, Security, status
)
from fastapi.responses import JSONResponse

from backend.app.models.pqr import PQRCreate, PQROut
from backend.app.logic.universal_controller_instance import universal_controller as controller
#from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/pqr", tags=["pqr"])

@router.get("/administrador/crear", response_class=JSONResponse)
def index_create_admin():
    """
    Devuelve el siguiente ID disponible para crear un PQR (admin).
    """
    try:
        pqrs = controller.read_all(PQROut)
        ultimo_id = max(p["ID"] for p in pqrs) if pqrs else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return JSONResponse(content={"nuevo_id": nuevo_id, "message": "Formulario de creación de PQR (admin) habilitado."})

@router.get("/pasajero/crear", response_class=JSONResponse)
def index_create_pasajero():
    """
    Devuelve el siguiente ID disponible para crear un PQR (pasajero).
    """
    try:
        pqrs = controller.read_all(PQROut)
        ultimo_id = max(p["ID"] for p in pqrs) if pqrs else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return JSONResponse(content={"nuevo_id": nuevo_id, "message": "Formulario de creación de PQR (pasajero) habilitado."})

@router.get("/administrador/actualizar", response_class=JSONResponse)
def index_update_admin():
    """
    Devuelve mensaje de habilitación de formulario de actualización (admin).
    """
    return JSONResponse(content={"message": "Formulario de actualización de PQR (admin) habilitado."})

@router.get("/administrador/eliminar", response_class=JSONResponse)
def index_delete_admin():
    """
    Devuelve mensaje de habilitación de formulario de eliminación (admin).
    """
    return JSONResponse(content={"message": "Formulario de eliminación de PQR (admin) habilitado."})

@router.post("/create", response_class=JSONResponse)
async def create_pqr(
    ID: int = Form(...),
    type: str = Form(...),
    description: str = Form(...),
    fecha: str = Form(...),
    identificationuser: int = Form(...),
):
    try:
        existing_pqr = controller.get_by_column(PQROut, "ID", ID)
        if existing_pqr:
            logger.warning(f"[POST /create] Error de validación: El PQR ya existe con ID {ID}")
            raise HTTPException(400, detail="El PQR ya existe con la misma identificación.")

        new_pqr = PQRCreate(ID=ID, type=type, description=description, fecha=fecha, identificationuser=identificationuser)
        controller.add(new_pqr)
        logger.info(f"[POST /create] PQR creado exitosamente con ID {ID}")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "operation": "create",
                "success": True,
                "data": PQROut(
                    ID=new_pqr.ID,
                    type=new_pqr.type,
                    description=new_pqr.description,
                    fecha=new_pqr.fecha,
                    identificationuser=new_pqr.identificationuser
                ).model_dump(),
                "message": "PQR created successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@router.post("/update", response_class=JSONResponse)
async def update_pqr(
    ID: int = Form(...),
    type: str = Form(...),
    description: str = Form(...),
    fecha: str = Form(...),
    identificationuser: int = Form(...),
):
    try:
        existing = controller.get_by_column(PQROut, "ID", ID)
        if existing is None:
            logger.warning(f"[POST /update] PQR no encontrada: ID={ID}")
            raise HTTPException(404, detail="PQR not found")

        updated_pqr = PQROut(ID=ID, type=type, description=description, fecha=fecha, identificationuser=identificationuser)
        controller.update(updated_pqr)
        logger.info(f"[POST /update] PQR actualizada exitosamente: {updated_pqr}")
        return JSONResponse(
            content={
                "operation": "update",
                "success": True,
                "data": updated_pqr.model_dump(),
                "message": f"PQR {ID} updated successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))

@router.post("/delete", response_class=JSONResponse)
async def delete_pqr(
    ID: int = Form(...),
):
    try:
        existing = controller.get_by_column(PQROut, "ID", ID)
        if not existing:
            logger.warning(f"[POST /delete] PQR no encontrado en la base de datos: ID={ID}")
            raise HTTPException(404, detail="PQR not found")
        controller.delete(existing)
        logger.info(f"[POST /delete] PQR eliminada exitosamente: ID={ID}")
        return JSONResponse(
            content={
                "operation": "delete",
                "success": True,
                "message": f"PQR {ID} deleted successfully."
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")