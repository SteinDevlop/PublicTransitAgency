from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from backend.app.models.payments import Payments
from backend.app.models.card import Card
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn
app = FastAPI(
    title="Consulta de Pagos",
    description="Microservicio para consultar pagos realizados con tarjetas",
    version="1.0.0"
)

controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/payments", response_class=HTMLResponse)
async def get_all_payments(request: Request):
    dummy = Payments(
        user="",
        payment_quantity=0,
        payment_method=False,
        vehicle_type="",
        card=Card(id="", tipo="", balance=0)
    )
    pagos = controller.read_all(dummy)
    return templates.TemplateResponse("ListaPagos.html", {"request": request, "pagos": pagos})

@app.get("/payments/{payment_id}", response_class=HTMLResponse)
async def get_payment_by_id(request: Request, payment_id: str):
    payment = controller.get_by_id(Payments, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return templates.TemplateResponse("DetallePago.html", {"request": request, "pago": payment})

@app.get("/payments/card/{card_id}", response_class=HTMLResponse)
async def get_payments_by_card(request: Request, card_id: str):
    card = controller.get_by_id(Card, card_id)
    if not card:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    
    dummy = Payments(
        user="",
        payment_quantity=0,
        payment_method=False,
        vehicle_type="",
        card=Card(id="", tipo="", balance=0)
    )
    all_payments = controller.read_all(dummy)
    pagos = [p for p in all_payments if p.card.id == card_id]
    return templates.TemplateResponse("PagosPorTarjeta.html", {"request": request, "pagos": pagos, "card_id": card_id})

if __name__ == "__main__":
    uvicorn.run("incidence_query_service:app", host="0.0.0.0", port=8003, reload=True)
