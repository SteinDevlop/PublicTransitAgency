import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.payments import Payment

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/payments", tags=["payments"])

@app.get("/", response_class=JSONResponse)
def listar_pagos():
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
def detalle_pago(ID: int):
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
            return {"message": "Detalle de pago consultado exitosamente.", "data": pago.model_dump()}
        elif hasattr(pago, "dict"):
            return {"message": "Detalle de pago consultado exitosamente.", "data": pago.dict()}
        else:
            return {"message": "Detalle de pago consultado exitosamente.", "data": pago}
    except Exception as e:
        logger.error("[GET /payments/{ID}] Error al consultar detalle de pago: %s", e)
        return JSONResponse(
            status_code=500,
            content={"detail": "Error al consultar detalle de pago."}
        )