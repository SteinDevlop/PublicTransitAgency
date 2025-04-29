from fastapi import FastAPI, HTTPException
from datetime import datetime
from uuid import uuid4
from src.backend.app.models.payments import Payments
from models.card import Card
from logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()

MIN_VALOR = 1000
MAX_VALOR = 100000

@app.post("/payment/tarjeta/{id}/recarga")
async def recharge(id: str, valor: float, tipo_transporte: str = "virtual"):
    if valor < MIN_VALOR or valor > MAX_VALOR:
        raise HTTPException(400, f"El valor debe estar entre {MIN_VALOR} y {MAX_VALOR}")

    tarjeta = controller.get_by_id(Card, id)
    if not tarjeta:
        raise HTTPException(404, "Tarjeta no encontrada")

    tarjeta.balance += valor
    controller.update(tarjeta)

    pago = Payments(
        user=str(uuid4()),
        payment_quantity=valor,
        payment_method=True,
        vehicle_type=tipo_transporte,
        card=tarjeta
    )
    controller.add(pago)

    return {
        "message": "Recarga exitosa",
        "new_balance": tarjeta.balance,
        "receipt": str(pago)
    }

@app.post("/tarjeta/{id}/uso")
async def use(id: str, valor: float, tipo_transporte: str):
    tarjeta = controller.get_by_id(Card, id)
    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    if tarjeta.balance < valor:
        raise HTTPException(
            status_code=400,
            detail="Saldo insuficiente"
        )

    tarjeta.balance -= valor
    controller.update(tarjeta)

    fecha = datetime.now().isoformat()
    pago = Payments(
        user=str(uuid4()),
        payment_quantity=valor,
        payment_method=True,
        vehicle_type=tipo_transporte,
        card=tarjeta
    )
    controller.add(pago)

    return {
        "message": "Uso registrado",
        "remaining_balance": tarjeta.balance,
        "receipt": str(pago)
    }

@app.get("/schema/payment")
async def get_schema():
    return {
        "fields": [
            {"name": "id", "type": "string", "required": True},
            {"name": "valor", "type": "number", "required": True},
            {"name": "tipo_transporte", "type": "string", "required": False}
        ]
    }

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
