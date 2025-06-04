import logging
from fastapi import APIRouter, HTTPException, Security
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.payments import Payment
from backend.app.core.auth import get_current_user

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
glob="Detalle pago consultado exitosamente."

app = APIRouter(prefix="/payments", tags=["payments"])

@app.get("/", response_class=JSONResponse)
def listar_pagos(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operario"])
):
    try:
        pagos = controller.read_all(Payment)
        logger.info("[GET /payments/] Pagos listados.")
        pagos_json = [
            p.model_dump() if hasattr(p, "model_dump")
            else p.dict() if hasattr(p, "dict")
            else p
            for p in pagos
        ]
        return {"message": "Pagos listados exitosamente.", "data": pagos_json}
    except Exception as e:
        logger.error("[GET /payments/] Error al listar pagos: %s", e)
        return JSONResponse(
            status_code=500,
            content={"detail": "Error al listar pagos."}
        )

@app.get("/{ID}", response_class=JSONResponse)
def detalle_pago(
    ID: int,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "operario"])
):
    try:
        pago = controller.get_by_id(Payment, ID)
        if not pago:
            logger.warning("[GET /payments/{ID}] Pago no encontrado: ID=%s", ID)
            return JSONResponse(
                status_code=404,
                content={"detail": "Pago no encontrado."}
            )
        logger.info("[GET /payments/{ID}] Detalle de pago consultado: ID=%s", ID)
        if hasattr(pago, "model_dump"):
            return {"message": glob, "data": pago.model_dump()}
        elif hasattr(pago, "dict"):
            return {"message": glob, "data": pago.dict()}
        else:
            return {"message": glob, "data": pago}
    except Exception as e:
        logger.error("[GET /payments/{ID}] Error al consultar detalle de pago: %s", e)
        return JSONResponse(
            status_code=500,
            content={"detail": "Error al consultar detalle de pago."}
        )