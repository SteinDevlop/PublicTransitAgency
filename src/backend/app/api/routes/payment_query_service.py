from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.payments import Payment

app = APIRouter(prefix="/payments", tags=["payments"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/", response_class=HTMLResponse)
def listar_pagos(request: Request):
    pagos = controller.read_all(Payment)
    return templates.TemplateResponse("ListarPagos.html", {"request": request, "pagos": pagos})

@app.get("/{id}", response_class=HTMLResponse)
def detalle_pago(id: int, request: Request):
    pago = controller.get_by_id(Payment, id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return templates.TemplateResponse("DetallePago.html", {"request": request, "pago": pago})