import logging
from fastapi import (
    Form, HTTPException, APIRouter, Security, status
)
from fastapi.responses import JSONResponse

from backend.app.models.price import PriceCreate, PriceOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/price", tags=["price"])

@router.get("/administrador/crear", response_class=JSONResponse)
def index_create(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        prices = controller.read_all(PriceOut)
        ultimo_id = max(p["ID"] for p in prices) if prices else 0
        nuevo_id = ultimo_id + 1
    except Exception as e:
        logger.error(f"Error al obtener el último ID: {str(e)}")
        nuevo_id = 1  # Por defecto

    return JSONResponse(content={"nuevo_id": nuevo_id, "message": "Formulario de creación de precio habilitado."})

@router.get("/administrador/actualizar", response_class=JSONResponse)
def index_update(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    return JSONResponse(content={"message": "Formulario de actualización de precio habilitado."})

@router.get("/administrador/eliminar", response_class=JSONResponse)
def index_delete(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    return JSONResponse(content={"message": "Formulario de eliminación de precio habilitado."})

@router.post("/create", response_class=JSONResponse)
async def create_price(
    ID: int = Form(...),
    IDTipoTransporte: int = Form(...),
    Monto: float = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existing_price = controller.get_by_column(PriceOut, "ID", ID)
        if existing_price:
            logger.warning(f"[POST /create] Error de validación: El precio ya existe con identificación {ID}")
            raise HTTPException(400, detail="El precio ya existe con la misma identificación.")

        new_price = PriceCreate(ID=ID, IDTipoTransporte=IDTipoTransporte, Monto=Monto)
        logger.info(f"Intentando insertar precio con datos: {new_price.model_dump()}")
        controller.add(new_price)
        logger.info(f"[POST /create] Precio creado exitosamente con identificación {ID}")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "operation": "create",
                "success": True,
                "data": PriceOut(ID=new_price.ID, IDTipoTransporte=new_price.IDTipoTransporte, Monto=new_price.Monto).model_dump(),
                "message": "Price created successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /create] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        logger.error(f"[POST /create] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@router.post("/update", response_class=JSONResponse)
async def update_price(
    ID: int = Form(...),
    IDTipoTransporte: int = Form(...),
    Monto: float = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existing = controller.get_by_column(PriceOut, "ID", ID)
        if existing is None:
            logger.warning(f"[POST /update] Precio no encontrada: id={ID}")
            raise HTTPException(404, detail="Price not found")

        updated_price = PriceOut(ID=ID, IDTipoTransporte=IDTipoTransporte, Monto=Monto)
        controller.update(updated_price)
        logger.info(f"[POST /update] Precio actualizada exitosamente: {updated_price}")
        return JSONResponse(
            content={
                "operation": "update",
                "success": True,
                "data": updated_price.model_dump(),
                "message": f"Price {ID} updated successfully."
            }
        )
    except ValueError as e:
        logger.warning(f"[POST /update] Error de validación: {str(e)}")
        raise HTTPException(400, detail=str(e))

@router.post("/delete", response_class=JSONResponse)
async def delete_price(
    ID: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    try:
        existing = controller.get_by_column(PriceOut, "ID", ID)
        if not existing:
            logger.warning(f"[POST /delete] Precio no encontrado en la base de datos: id={ID}")
            raise HTTPException(404, detail="Price not found")

        logger.info(f"[POST /delete] Eliminando precio con ID={ID}")
        controller.delete(existing)
        logger.info(f"[POST /delete] Precio eliminada exitosamente: id={ID}")
        return JSONResponse(
            content={
                "operation": "delete",
                "success": True,
                "message": f"Price {ID} deleted successfully."
            }
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"[POST /delete] Error interno: {str(e)}")
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")