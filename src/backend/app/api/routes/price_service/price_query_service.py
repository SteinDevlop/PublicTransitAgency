import logging
from fastapi import APIRouter, Security, Query, HTTPException
from fastapi.responses import JSONResponse

from backend.app.core.auth import get_current_user
from backend.app.models.price import PriceOut
from backend.app.logic.universal_controller_instance import universal_controller as controller

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

router = APIRouter(prefix="/price", tags=["price"])

@router.get("/pasajero/consultar", response_class=JSONResponse)
def consultar_pasajero(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Mensaje para consulta de precios de pasajero.
    """
    return JSONResponse(content={"message": "Consulta de precio para pasajero habilitada."})

@router.get("/pasajero/prices", response_class=JSONResponse)
def get_prices_pasajero(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve todos los precios (pasajero).
    """
    prices = controller.read_all(PriceOut)
    logger.info(f"[GET /pasajero/prices] Número de precios encontrados: {len(prices) if prices else 0}")
    return JSONResponse(content={"prices": prices or []})

@router.get("/administrador/consultar", response_class=JSONResponse)
def consultar_admin(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Mensaje para consulta de precios de administrador.
    """
    return JSONResponse(content={"message": "Consulta de precio para administrador habilitada."})

@router.get("/administrador/prices", response_class=JSONResponse)
def get_prices_admin(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve todos los precios (administrador).
    """
    prices = controller.read_all(PriceOut)
    logger.info(f"[GET /administrador/prices] Número de precios encontrados: {len(prices) if prices else 0}")
    return JSONResponse(content={"prices": prices or []})

@router.get("/administrador/precio", response_class=JSONResponse)
def price_admin(
    id: int = Query(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Devuelve un precio específico por ID (administrador).
    """
    unit_price = controller.get_by_column(PriceOut, "ID", id)
    if not unit_price:
        logger.warning(f"[GET /administrador/precio] No se encontró precio con id={id}")
        raise HTTPException(status_code=404, detail="Precio no encontrado")
    logger.info(f"[GET /administrador/precio] Precio encontrado: {unit_price.ID}, {unit_price.IDTipoTransporte},{unit_price.Monto}")
    return JSONResponse(content=unit_price.model_dump())