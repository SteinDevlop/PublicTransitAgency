from fastapi import FastAPI, Form, Request, HTTPException, APIRouter, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.payments import PaymentOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/payments", tags=["payments"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get('/consultar', response_class=HTMLResponse)
def consultar(request: Request):
    """Renders the 'ConsultarPagos.html' template."""
    return templates.TemplateResponse("ConsultarPagos.html", {"request": request})

@app.get("/{payment_id}", response_class=HTMLResponse)
async def get_payment_by_id(request: Request, payment_id: int):
    """Retrieves a payment by its ID and renders it using a template."""
    payment = controller.get_by_id(PaymentOut, payment_id)
    if payment:
        return templates.TemplateResponse("pago.html", {
            "request": request,
            "payment": payment
        })
    raise HTTPException(status_code=404, detail="Payment not found") # Devolver 404 si no se encuentra
