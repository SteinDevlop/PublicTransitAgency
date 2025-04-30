from fastapi import FastAPI, Request, HTTPException, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from backend.app.models.payments import Payments, PaymentsOut  # Asegúrate de tener un PaymentsOut model
from backend.app.models.card import Card, CardOut  # Asegúrate de tener un CardOut model
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn

# Initialize the FastAPI router for the "payments" functionality
app = APIRouter(prefix="/payments", tags=["pagos"])

controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/schema", response_model=dict)
async def get_payment_schema():
    """Retorna el esquema de la entidad de pagos."""
    return {
        "name": "payments",
        "fields": [
            {"name": "id", "type": "string", "required": True},
            {"name": "user", "type": "string", "required": True},
            {"name": "payment_quantity", "type": "number", "required": True},
            {"name": "payment_method", "type": "bool", "required": True},
            {"name": "vehicle_type", "type": "string", "required": True},
            {"name": "card_id", "type": "string", "required": True}  # Usar card_id para la relación
        ]
    }

@app.get("", response_class=HTMLResponse)
async def listar_pagos_html(request: Request):
    """Lista todos los pagos en formato HTML."""
    pagos = controller.read_all(PaymentsOut)
    return templates.TemplateResponse("ListarPagos.html", {"request": request, "pagos": pagos})

@app.get("/json")
async def listar_pagos_json():
    """Lista todos los pagos en formato JSON."""
    pagos = controller.read_all(PaymentsOut)
    return JSONResponse(content={"data": pagos})

@app.get("/{payment_id}", response_class=HTMLResponse)
async def obtener_pago_html(request: Request, payment_id: str):
    """Obtiene un pago por su ID y lo muestra en HTML."""
    pago = controller.get_by_id(PaymentsOut, payment_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return templates.TemplateResponse("DetallePago.html", {"request": request, "pago": pago})

@app.get("/{payment_id}/json")
async def obtener_pago_json(payment_id: str):
    """Obtiene un pago por su ID en formato JSON."""
    pago = controller.get_by_id(PaymentsOut, payment_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return JSONResponse(content={"data": pago.dict()})

@app.get("/tarjeta/{card_id}", response_class=HTMLResponse)
async def obtener_pagos_por_tarjeta_html(request: Request, card_id: str):
    """Obtiene los pagos asociados a una tarjeta y los muestra en HTML."""
    tarjeta = controller.get_by_id(CardOut, card_id)
    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    todos_los_pagos = controller.read_all(PaymentsOut)
    pagos = [p for p in todos_los_pagos if p.card_id == card_id] # Asumiendo que PaymentsOut tiene card_id
    return templates.TemplateResponse("PagoPorTarjeta.html", {"request": request, "pagos": pagos, "card_id": card_id})

@app.get("/tarjeta/{card_id}/json")
async def obtener_pagos_por_tarjeta_json(card_id: str):
    """Obtiene los pagos asociados a una tarjeta en formato JSON."""
    tarjeta = controller.get_by_id(CardOut, card_id)
    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    todos_los_pagos = controller.read_all(PaymentsOut)
    pagos = [p for p in todos_los_pagos if p.card_id == card_id] # Asumiendo que PaymentsOut tiene card_id
    return JSONResponse(content={"data": [p.dict() for p in pagos]})

if __name__ == "__main__":
    app_main = FastAPI(
        title="Consulta de Pagos",
        description="Microservicio para consultar pagos realizados con tarjetas",
        version="1.0.0"
    )
    app_main.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app_main.include_router(app)
    uvicorn.run(app_main, host="0.0.0.0", port=8003, reload=True)