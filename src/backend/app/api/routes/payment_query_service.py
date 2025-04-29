from fastapi import FastAPI, HTTPException
from src.backend.app.models.payments import Payments
from models.card import Card
from logic.universal_controller_sql import UniversalController  

app = FastAPI()
controller = UniversalController()  

@app.get("/schema/payments")
async def get_payment_schema():
    return {
        "name": "payments",
        "fields": [
            {"name": "id", "type": "string", "required": True},
            {"name": "user", "type": "string", "required": True},
            {"name": "payment_quantity", "type": "number", "required": True},
            {"name": "payment_method", "type": "bool", "required": True},
            {"name": "vehicle_type", "type": "string", "required": True},
            {"name": "card", "type": "string", "required": True}
        ]
    }

@app.get("/payments")
async def get_all_payments():
    dummy = Payments(
        user="",
        payment_quantity=0,
        payment_method=False,
        vehicle_type="",
        card=Card(id="", tipo="", balance=0)
    )
    return controller.read_all(dummy)

@app.get("/payments/{payment_id}")
async def get_payment(payment_id: str):
    payment = controller.get_by_id(Payments, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return payment

@app.get("/payments/card/{card_id}")
async def get_payments_by_card(card_id: str):
    card = controller.get_by_id(Card, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    all_payments = controller.read_all(Payments(
        user="",
        payment_quantity=0,
        payment_method=False,
        vehicle_type="",
        card=Card(id="", tipo="", balance=0)
    ))
    return [p for p in all_payments if p.card.id == card_id]
