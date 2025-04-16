from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from uuid import uuid4
import payment_service_recharge as recharge_service

from logic.payments import Payments
from logic.universal_controller_json import UniversalController
from logic.card import Card  

app = FastAPI()
controller = UniversalController()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MIN_VALOR = 1000
MAX_VALOR = 100000



@app.post('/payment/tarjeta/{id}/uso')
def use(id: str, valor: float, tipo_transporte: str):
    tarjeta = controller.get_by_id(Card, id)
    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    if tarjeta.saldo < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    tarjeta.saldo -= valor
    controller.update(tarjeta)

    fecha = datetime.now().isoformat()
    pago = Payments(str(uuid4()), id, tipo_transporte, "uso", valor, fecha)
    controller.add(pago)

    recharge_service.generar_registro(id, tipo_transporte, "uso", valor, fecha)

    return {"mensaje": "Uso registrado", "saldo_restante": tarjeta.saldo}

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
