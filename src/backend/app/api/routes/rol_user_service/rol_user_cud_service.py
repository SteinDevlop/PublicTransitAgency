import logging
from fastapi import (
    Form, HTTPException, APIRouter, Security, status
)
from fastapi.responses import JSONResponse

from backend.app.models.rol_user import RolUserCreate, RolUserOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/roluser", tags=["roluser"])

@router.get("/crear", response_class=JSONResponse)
def index_create(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        rolusers = controller.read_all(RolUserOut)
        ultimo_id = max(p["ID"] for p in rolusers) if rolusers else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return JSONResponse(content={"nuevo_id": nuevo_id, "message": "Formulario de creación de rol de usuario habilitado."})

@router.get("/actualizar", response_class=JSONResponse)
def index_update(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    return JSONResponse(content={"message": "Formulario de actualización de rol de usuario habilitado."})

@router.get("/eliminar", response_class=JSONResponse)
def index_delete(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    return JSONResponse(content={"message": "Formulario de eliminación de rol de usuario habilitado."})

@router.post("/create", response_class=JSONResponse)
async def create_roluser(
    ID: int = Form(...),
    Rol: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existing_user = controller.get_by_column(RolUserOut, "Rol", Rol)
        if existing_user:
            logger.warning(f"[POST /create] Error de validación: El rol de usuario ya existe con ID {ID}")
            raise HTTPException(400, detail="El rol de usuario ya existe con la misma identificación.")

        new_roluser = RolUserCreate(ID=ID, Rol=Rol)
        logger.info(f"Intentando insertar rol de usuario con datos: {new_roluser.model_dump()}")
        controller.add(new_roluser)
        logger.info(f"Rol de Usuario insertado con ID: {new_roluser.ID}")
        logger.info(f"[POST /create] Rol de Usuario creado exitosamente con identificación {ID}")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "operation": "create",
                "success": True,
                "data": RolUserOut(ID=new_roluser.ID, Rol=new_roluser.Rol).model_dump(),
                "message": "RolUser created successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@router.post("/update", response_class=JSONResponse)
async def update_roluser(
    ID: int = Form(...),
    Rol: str = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existing = controller.get_by_column(RolUserOut, "ID", ID)
        if existing is None:
            logger.warning(f"[POST /update] Rol de Usuario no encontrada: ID={ID}")
            raise HTTPException(404, detail="RolUser not found")

        updated_roluser = RolUserOut(ID=ID, Rol=Rol)
        controller.update(updated_roluser)
        logger.info(f"[POST /update] RolUser actualizada exitosamente: {updated_roluser}")
        return JSONResponse(
            content={
                "operation": "update",
                "success": True,
                "data": updated_roluser.model_dump(),
                "message": f"RolUser {ID} updated successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))

@router.post("/delete", response_class=JSONResponse)
async def delete_roluser(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existing = controller.get_by_column(RolUserOut, "ID", ID)
        if not existing:
            logger.warning(f"[POST /delete] Rol de Usuario no encontrado en la base de datos: ID={ID}")
            raise HTTPException(404, detail="RolUser not found")

        logger.info(f"[POST /delete] Eliminando rol de usuario con ID={ID}")
        controller.delete(existing)
        logger.info(f"[POST /delete] Rol de Usuario eliminada exitosamente: ID={ID}")
        return JSONResponse(
            content={
                "operation": "delete",
                "success": True,
                "message": f"RolUser {ID} deleted successfully."
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")