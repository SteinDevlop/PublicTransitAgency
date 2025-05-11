from fastapi import APIRouter, Form, HTTPException, Request, Security
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.logic.universal_controller_sqlserver import UniversalController
from backend.app.models.payments import Payment
from backend.app.core.auth import get_current_user

app = APIRouter(prefix="/payments", tags=["payments"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/create", response_class=HTMLResponse)
def crear_pago_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "finanzas"])
):
    """
    Renderiza el formulario para crear un nuevo pago.
    """
    return templates.TemplateResponse("CrearPago.html", {"request": request})

@app.post("/create")
def crear_pago(
    IDMovimiento: int = Form(...),
    IDPago: int = Form(...),
    IDTarjeta: int = Form(...),
    IDTransporte: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "finanzas"])
):
    """
    Crea un nuevo pago.
    """
    pago = Payment(IDMovimiento=IDMovimiento, IDPago=IDPago, IDTarjeta=IDTarjeta, IDTransporte=IDTransporte)
    try:
        controller.add(pago)
        return {"message": "Pago creado exitosamente.", "data": pago.to_dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/delete", response_class=HTMLResponse)
def eliminar_pago_form(
    request: Request,
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "finanzas"])
):
    """
    Renderiza el formulario para eliminar un pago.
    """
    return templates.TemplateResponse("EliminarPago.html", {"request": request})

@app.post("/delete")
def eliminar_pago(
    IDMovimiento: int = Form(...),
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "finanzas"])
):
    """
    Elimina un pago por su IDMovimiento.
    """
    try:
        controller.delete(Payment(IDMovimiento=IDMovimiento))
        return {"message": "Pago eliminado exitosamente."}
    except ValueError:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
