import logging
import re
from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.payments import Payment

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/payments", tags=["payments"])

@app.post("/create", response_class=JSONResponse)
def crear_pago(
    IDMovimiento: int = Form(...),
    IDPrecio: int = Form(...),
    IDTarjeta: int = Form(...),
    IDUnidad: str = Form("EMPTY"),
    ID: int = Form(...),
):
    safe_unidad = re.sub(r"[^\w\-]", "_", IDUnidad)
    try:
        pago = Payment(
            IDMovimiento=IDMovimiento,
            IDPrecio=IDPrecio,
            IDTarjeta=IDTarjeta,
            IDUnidad=safe_unidad,
            ID=ID
        )
        controller.add(pago)
        logger.info("[POST /payments/create] Pago creado exitosamente: ID=%s", ID)
        return JSONResponse(content={"message": "Pago creado exitosamente.", "data": pago.model_dump()})
    except ValueError as e:
        logger.warning("[POST /payments/create] Error al crear pago: %s", e)
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/update", response_class=JSONResponse)
def actualizar_pago(
    ID: int = Form(...),
    IDMovimiento: int = Form(...),
    IDPrecio: int = Form(...),
    IDTarjeta: int = Form(...),
    IDUnidad: str = Form(...),
):
    try:
        existing = controller.get_by_id(Payment, ID)
        if not existing:
            logger.warning("[POST /payments/update] Pago no encontrado: ID=%s", ID)
            raise HTTPException(status_code=404, detail="Pago no encontrado")
        pago = Payment(
            ID=ID,
            IDMovimiento=IDMovimiento,
            IDPrecio=IDPrecio,
            IDTarjeta=IDTarjeta,
            IDUnidad=IDUnidad
        )
        controller.update(pago)
        logger.info("[POST /payments/update] Pago actualizado exitosamente: ID=%s", ID)
        return JSONResponse(content={"message": "Pago actualizado exitosamente."})
    except HTTPException:
        raise
    except Exception as e:
        logger.error("[POST /payments/update] Error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/delete", response_class=JSONResponse)
def eliminar_pago(ID: int = Form(...)):
    try:
        existing = controller.get_by_id(Payment, ID)
        if not existing:
            logger.warning("[POST /payments/delete] Pago no encontrado: ID=%s", ID)
            raise HTTPException(status_code=404, detail="Pago no encontrado")
        pago = Payment(ID=ID, IDMovimiento=0, IDPrecio=0, IDTarjeta=0, IDUnidad="EMPTY")
        controller.delete(pago)
        logger.info("[POST /payments/delete] Pago eliminado exitosamente: ID=%s", ID)
        return JSONResponse(content={"message": "Pago eliminado exitosamente."})
    except HTTPException:
        raise
    except Exception as e:
        logger.error("[POST /payments/delete] Error: %s", e)
        raise HTTPException(status_code=500, detail=str(e))