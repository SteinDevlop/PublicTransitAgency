from fastapi import FastAPI, HTTPException
from src.backend.app.models.payments import Payments
from models.card import Card
from logic.universal_controller_sql import UniversalController  

app = FastAPI()
controller = UniversalController()  

@app.get("/payment/schema/pagos")
async def get_payment_schema():
    return {
        "name": "pagos",
        "fields": [
            {"name": "id", "type": "str", "required": True},
            {"name": "user", "type": "str", "required": True},
            {"name": "payment_quantity", "type": "float", "required": True},
            {"name": "payment_method", "type": "bool", "required": True},
            {"name": "vehicle_type", "type": "int", "required": True},
            {"name": "card", "type": "Card", "required": True}
        ]
    }

@app.get("/payment/")
async def get_all_payments():
    dummy = Payments(
        user="",
        payment_quantity=0,
        payment_method=False,
        vehicle_type=0,
        card=Card(id=0, tipo="", balance=0)
    )
    return controller.read_all(dummy)

app.get("/{payment_id}", response_model=Payments)
async def get_payment(payment_id: str):
    """Obtener un pago específico"""
    payment = controller.get_by_id(Payments, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return payment

@app.get("/tarjeta/{card_id}", response_model=list[Payments])
async def get_payments_by_card(card_id: str):
    """Obtener todos los pagos de una tarjeta"""
    card = controller.get_by_id(Card, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    all_payments = await get_all_payments()
    return [p for p in all_payments if p.card.id == card_id]
