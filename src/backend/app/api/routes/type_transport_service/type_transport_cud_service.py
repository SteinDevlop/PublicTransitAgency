import logging
from fastapi import (
    Form, HTTPException, APIRouter, Security, status
)
from fastapi.responses import JSONResponse

from backend.app.models.type_transport import TypeTransportCreate, TypeTransportOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/typetransport", tags=["typetransport"])

@router.get("/crear", response_class=JSONResponse)
def index_create(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    return JSONResponse(content={"message": "Formulario de creación de tipo de transporte habilitado."})

@router.get("/actualizar", response_class=JSONResponse)
def index_update(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    return JSONResponse(content={"message": "Formulario de actualización de tipo de transporte habilitado."})

@router.get("/eliminar", response_class=JSONResponse)
def index_delete(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    return JSONResponse(content={"message": "Formulario de eliminación de tipo de transporte habilitado."})

@router.post("/create", response_class=JSONResponse)
async def create_typetransport(
    ID: int = Form(...),
    TipoTransporte: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existing_transport = controller.get_by_column(TypeTransportOut, "TipoTransporte", TipoTransporte)
        if existing_transport:
            logger.warning(f"[POST /create] Error de validación: El tipo de transporte ya existe con ID {ID}")
            raise HTTPException(400, detail="El tipo de transporte ya existe con la misma identificación.")

        new_typetransport = TypeTransportCreate(ID=ID, TipoTransporte=TipoTransporte)
        logger.info(f"Intentando insertar tipo de transporte con datos: {new_typetransport.model_dump()}")
        controller.add(new_typetransport)
        logger.info(f"Tipo de Transporte insertado con ID: {new_typetransport.ID}")
        logger.info(f"[POST /create] Tipo de Transporte creado exitosamente con identificación {ID}")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "operation": "create",
                "success": True,
                "data": TypeTransportOut(
                    ID=new_typetransport.ID,
                    TipoTransporte=new_typetransport.TipoTransporte
                ).model_dump(),
                "message": "TypeTransport created successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@router.post("/update", response_class=JSONResponse)
async def update_typetransport(
    ID: int = Form(...),
    TipoTransporte: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existing = controller.get_by_id(TypeTransportOut, ID)
        if existing is None:
            logger.warning(f"[POST /update] Tipo de Transporte no encontrada: ID={ID}")
            raise HTTPException(404, detail="TypeTransport not found")

        updated_typetransport = TypeTransportOut(ID=ID, TipoTransporte=TipoTransporte)
        controller.update(updated_typetransport)
        logger.info(f"[POST /update] TipoTransporte actualizada exitosamente: {updated_typetransport}")
        return JSONResponse(
            content={
                "operation": "update",
                "success": True,
                "data": updated_typetransport.model_dump(),
                "message": f"TypeTransport {ID} updated successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))

@router.post("/delete", response_class=JSONResponse)
async def delete_typetransport(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existing = controller.get_by_id(TypeTransportOut, ID)
        if not existing:
            logger.warning(f"[POST /delete] Tipo de transporte no encontrado en la base de datos: ID={ID}")
            raise HTTPException(404, detail="TypeTransport not found")

        logger.info(f"[POST /delete] Eliminando tipo de transporte con ID={ID}")
        controller.delete(existing)
        logger.info(f"[POST /delete] Tipo de Transporte eliminada exitosamente: ID={ID}")
        return JSONResponse(
            content={
                "operation": "delete",
                "success": True,
                "message": f"TypeTransport {ID} deleted successfully."
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")