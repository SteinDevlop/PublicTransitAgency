import logging
from fastapi import (
    Form, HTTPException, APIRouter, Security, status
)
from fastapi.responses import JSONResponse

from backend.app.models.user import UserCreate, UserOut
from backend.app.models.rol_user import RolUserOut
from backend.app.models.shift import Shift
from backend.app.logic.universal_controller_instance import universal_controller as controller

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/crear", response_class=JSONResponse)
def index_create():
    try:
        users = controller.read_all(UserOut)
        roles = controller.read_all(RolUserOut)
        turnos = controller.read_all(Shift)
        ultimo_id = max(p["ID"] for p in users) if users else 0
        nuevo_id = ultimo_id + 1
        return JSONResponse(
            content={
                "nuevo_id": nuevo_id,
                "roles": roles or [],
                "turnos": turnos or []
            }
        )
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Error al obtener el último ID: {str(e)}"}
        )

@router.get("/actualizar", response_class=JSONResponse)
def index_update():
    return JSONResponse(content={"message": "Formulario de actualización de usuario habilitado."})

@router.get("/eliminar", response_class=JSONResponse)
def index_delete():
    return JSONResponse(content={"message": "Formulario de eliminación de usuario habilitado."})

@router.post("/create", response_class=JSONResponse)
async def create_user(
    ID: int = Form(...),
    Identificacion: int = Form(...),
    Nombre: str = Form(...),
    Apellido: str = Form(...),
    Correo: str = Form(...),
    Contrasena: str = Form(...),
    IDRolUsuario: int = Form(...),
    IDTurno: int = Form(...),
    IDTarjeta: int = Form(...),
):
    try:
        existing_user = controller.get_by_column(UserOut, "Identificacion", Identificacion)
        if existing_user:
            raise HTTPException(400, detail="El usuario ya existe con la misma identificación.")

        new_user = UserCreate(
            ID=ID,
            Identificacion=Identificacion,
            Nombre=Nombre,
            Apellido=Apellido,
            Correo=Correo,
            Contrasena=Contrasena,
            IDRolUsuario=IDRolUsuario,
            IDTurno=IDTurno,
            IDTarjeta=IDTarjeta
        )
        logger.info(f"Intentando insertar usuario con datos: {new_user.model_dump()}")
        controller.add(new_user)
        logger.info(f"Usuario insertado con ID: {new_user.ID}")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "operation": "create",
                "success": True,
                "data": UserOut(
                    ID=new_user.ID,
                    Identificacion=new_user.Identificacion,
                    Nombre=new_user.Nombre,
                    Apellido=new_user.Apellido,
                    Correo=new_user.Correo,
                    Contrasena=new_user.Contrasena,
                    IDRolUsuario=new_user.IDRolUsuario,
                    IDTurno=new_user.IDTurno,
                    IDTarjeta=new_user.IDTarjeta
                ).model_dump(),
                "message": "User created successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@router.post("/update", response_class=JSONResponse)
async def update_user(
    ID: int = Form(...),
    Identificacion: int = Form(...),
    Nombre: str = Form(...),
    Apellido: str = Form(...),
    Correo: str = Form(...),
    Contrasena: str = Form(...),
    IDRolUsuario: int = Form(...),
    IDTurno: int = Form(...),
    IDTarjeta: int = Form(...)
):
    try:
        existing = controller.get_by_column(UserOut, "ID", ID)
        if not existing:
            logger.warning(f"[POST /update] Usuario no encontrada: id={ID}")
            raise HTTPException(404, detail="User not found")

        updated_user = UserOut(
            ID=ID,
            Identificacion=Identificacion,
            Nombre=Nombre,
            Apellido=Apellido,
            Correo=Correo,
            Contrasena=Contrasena,
            IDRolUsuario=IDRolUsuario,
            IDTurno=IDTurno,
            IDTarjeta=IDTarjeta
        )
        controller.update(updated_user)
        logger.info(f"[POST /update] Usuario actualizada exitosamente: {updated_user}")
        return JSONResponse(
            content={
                "operation": "update",
                "success": True,
                "data": updated_user.model_dump(),
                "message": f"User {ID} updated successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))

@router.post("/delete", response_class=JSONResponse)
async def delete_user(
    ID: int = Form(...)
):
    try:
        existing = controller.get_by_column(UserOut, "ID", ID)
        if not existing:
            logger.warning(f"[POST /delete] Usuario no encontrado en la base de datos: id={ID}")
            raise HTTPException(404, detail="User not found")

        logger.info(f"[POST /delete] Eliminando usuario con id={ID}")
        controller.delete(existing)
        return JSONResponse(
            content={
                "operation": "delete",
                "success": True,
                "message": f"User {ID} deleted successfully."
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")