from fastapi import FastAPI, Form, HTTPException, APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from backend.app.models.payments import PaymentCreate, PaymentOut
from backend.app.logic.universal_controller_sql import UniversalController
import datetime

app = APIRouter(prefix="/payments", tags=["payments"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/crear", response_class=HTMLResponse)
def index_create(request: Request):
    return templates.TemplateResponse("CrearPago.html", {"request": request}) 

@app.get("/actualizar", response_class=HTMLResponse)
def index_update(request: Request):
    return templates.TemplateResponse("ActualizarPago.html", {"request": request}) 

@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(request: Request):
    return templates.TemplateResponse("EliminarPago.html", {"request": request}) 

@app.post("/create")
async def create_payment(
    user: str = Form(...),
    payment_quantity: float = Form(...),
    payment_method: bool = Form(...),
    vehicle_type: int = Form(...),
    card_id: int = Form(...),
):
    try:
        new_payment = PaymentCreate(
            date=datetime.datetime.now(),
            user=user,
            payment_quantity=payment_quantity,
            payment_method=payment_method,
            vehicle_type=vehicle_type,
            card_id=card_id
        )
        result = controller.add(new_payment)
        return {"operation": "create", "success": True, "data": PaymentOut(**result.to_dict()).dict(), "message": "Payment created successfully"}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@app.post("/update/{id}")
async def update_payment(
    id: int,
    user: str = Form(None),
    payment_quantity: float = Form(None),
    payment_method: bool = Form(None),
    vehicle_type: int = Form(None),
    card_id: int = Form(None),
    # user_auth = Depends(get_current_user) # Si tienes autenticación
):
    try:
        existing_payment = controller.get_by_id(PaymentOut, id)
        if not existing_payment:
            raise HTTPException(404, detail="Payment not found")

        update_data = PaymentCreate(
            date=existing_payment.date, # Keep existing date if not provided
            user=user if user is not None else existing_payment.user,
            payment_quantity=payment_quantity if payment_quantity is not None else existing_payment.payment_quantity,
            payment_method=payment_method if payment_method is not None else existing_payment.payment_method,
            vehicle_type=vehicle_type if vehicle_type is not None else existing_payment.vehicle_type,
            card_id=card_id if card_id is not None else existing_payment.card_id
        )
        update_data.id = id # Ensure ID is set for update
        result = controller.update(update_data)
        return {"operation": "update", "success": True, "data": PaymentOut(**result.to_dict()).dict(), "message": f"Payment {id} updated successfully"}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@app.post("/delete/{id}")
async def delete_payment(id: int):
    try:
        existing_payment = controller.get_by_id(PaymentOut, id)
        if not existing_payment:
            raise HTTPException(404, detail="Payment not found")
        controller.delete(existing_payment)
        return {"operation": "delete", "success": True, "message": f"Payment {id} deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=str(e))