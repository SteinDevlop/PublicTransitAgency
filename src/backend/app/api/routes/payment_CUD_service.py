from fastapi import FastAPI, Request, Form, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from backend.app.models.card import Card
from backend.app.models.payments import Payments
from backend.app.logic.universal_controller_sql import UniversalController
from uuid import uuid4
from datetime import datetime
import uvicorn

app = FastAPI(
    title="Servicio de Pagos y Recargas",
    description="Microservicio para gestionar recargas y usos de tarjetas de transporte",
    version="1.0.0"
)

controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constantes de validación
MIN_VALOR = 1000
MAX_VALOR = 100000

# Endpoints para formularios HTML
@app.get("/tarjeta/recarga", response_class=HTMLResponse)
async def mostrar_formulario_recarga(request: Request):
    return templates.TemplateResponse("RecargaTarjeta.html", {"request": request})

@app.get("/tarjeta/uso", response_class=HTMLResponse)
async def mostrar_formulario_uso(request: Request):
    return templates.TemplateResponse("UsoTarjeta.html", {"request": request})

# Endpoint para recarga de tarjeta
@app.post("/tarjeta/recarga", response_class=HTMLResponse)
async def recargar_tarjeta(
    request: Request, 
    id: str = Form(...),
    valor: float = Form(...),
    tipo_transporte: str = Form("virtual")
):
    if valor < MIN_VALOR or valor > MAX_VALOR:
        raise HTTPException(status_code=400, detail=f"El valor debe estar entre {MIN_VALOR} y {MAX_VALOR}")

    tarjeta = controller.get_by_id(Card, id)
    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

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

    return templates.TemplateResponse(
        "ResultadoOperacion.html",
        {
            "request": request,
            "titulo": "Recarga Exitosa",
            "mensaje": f"Se recargaron ${valor:,.2f} a la tarjeta {id}. Saldo actual: ${tarjeta.balance:,.2f}."
        }
    )

# Endpoint para uso de tarjeta
@app.post("/tarjeta/uso", response_class=HTMLResponse)
async def usar_tarjeta(
    request: Request,
    id: str = Form(...),
    valor: float = Form(...),
    tipo_transporte: str = Form(...)
):
    tarjeta = controller.get_by_id(Card, id)
    if not tarjeta:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")

    if tarjeta.balance < valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    tarjeta.balance -= valor
    controller.update(tarjeta)

    pago = Payments(
        user=str(uuid4()),
        payment_quantity=valor,
        payment_method=True,
        vehicle_type=tipo_transporte,
        card=tarjeta
    )
    controller.add(pago)

    return templates.TemplateResponse(
        "ResultadoOperacion.html",
        {
            "request": request,
            "titulo": "Uso Registrado",
            "mensaje": f"Se descontaron ${valor:,.2f} de la tarjeta {id}. Saldo restante: ${tarjeta.balance:,.2f}."
        }
    )

# Endpoint para consultar el saldo de una tarjeta
@app.get("/tarjeta/saldo", response_class=HTMLResponse)
async def consultar_saldo(
    request: Request,
    id: str = Query(..., description="ID de la tarjeta")
):
    tarjeta = controller.get_by_id(Card, id)
    if not tarjeta:
        return templates.TemplateResponse(
            "ResultadoOperacion.html",
            {
                "request": request,
                "titulo": "Tarjeta No Encontrada",
                "mensaje": f"No se encontró la tarjeta con ID {id}."
            },
            status_code=404
        )

    return templates.TemplateResponse(
        "ResultadoOperacion.html",
        {
            "request": request,
            "titulo": "Consulta de Saldo",
            "mensaje": f"El saldo actual de la tarjeta {id} es: ${tarjeta.balance:,.2f}."
        }
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)
