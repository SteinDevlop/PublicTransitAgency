from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.models.payments import Payment

app = APIRouter(prefix="/payments", tags=["payments"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_pago_form(request: Request):
    return templates.TemplateResponse("CrearPago.html", {"request": request})

@app.post("/create")
def crear_pago(
    id: int = Form(...),
    user: str = Form(...),
    payment_quantity: float = Form(...),
    payment_method: bool = Form(...),
    vehicle_type: int = Form(...),
    card_id: int = Form(...)
):
    pago = Payment(
        id=id,
        user=user,
        payment_quantity=payment_quantity,
        payment_method=payment_method,
        vehicle_type=vehicle_type,
        card_id=card_id
    )
    try:
        controller.add(pago)
        return {
            "operation": "create",
            "success": True,
            "data": pago,
            "message": "Pago creado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/update", response_class=HTMLResponse)
def actualizar_pago_form(request: Request):
    return templates.TemplateResponse("ActualizarPago.html", {"request": request})

@app.post("/update")
def actualizar_pago(
    id: int = Form(...),
    user: str = Form(...),
    payment_quantity: float = Form(...),
    payment_method: bool = Form(...),
    vehicle_type: int = Form(...),
    card_id: int = Form(...)
):
    pago = Payment(
        id=id,
        user=user,
        payment_quantity=payment_quantity,
        payment_method=payment_method,
        vehicle_type=vehicle_type,
        card_id=card_id
    )
    try:
        controller.update(pago)
        return {
            "operation": "update",
            "success": True,
            "data": pago,
            "message": "Pago actualizado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_pago_form(request: Request):
    return templates.TemplateResponse("EliminarPago.html", {"request": request})

@app.post("/delete")
def eliminar_pago(id: int = Form(...)):
    pago = Payment(id=id)
    try:
        controller.delete(pago)
        return {
            "operation": "delete",
            "success": True,
            "message": "Pago eliminado exitosamente."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))