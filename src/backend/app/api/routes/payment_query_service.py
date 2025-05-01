from fastapi import FastAPI, APIRouter, Request, Query
from fastapi.responses import HTMLResponse
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from backend.app.models.payments import PaymentOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/payments", tags=["payments"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/listar", response_class=HTMLResponse)
def list_payments_page(request: Request):
    payments = controller.read_all(PaymentOut)
    return templates.TemplateResponse("ListarPagos.html", {"request": request, "payments": payments})

@app.get("/detalles/{id}", response_class=HTMLResponse)
def payment_detail_page(request: Request, id: int):
    payment = controller.get_by_id(PaymentOut, id)
    return templates.TemplateResponse("DetallePago.html", {"request": request, "payment": payment})

@app.get("/all")
async def get_all_payments():
    return controller.read_all(PaymentOut)

@app.get("/{id}")
async def get_payment_by_id(id: int):
    payment = controller.get_by_id(PaymentOut, id)
    if payment:
        return payment
    raise HTTPException(404, detail="Payment not found")