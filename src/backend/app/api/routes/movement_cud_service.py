from fastapi import FastAPI, Form, HTTPException, APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.movement import MovementCreate, MovementOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/movement", tags=["movement"])
templates = Jinja2Templates(directory="src/backend/app/templates")

# --- Nuevo: Inyección de Dependencia ---
def get_controller():
    return UniversalController()

# Vistas HTML
@app.get("/crear", response_class=HTMLResponse)
def index_crear(request: Request):
    return templates.TemplateResponse("CrearMovimiento.html", {"request": request})

@app.get("/actualizar", response_class=HTMLResponse)
def index_actualizar(request: Request):
    return templates.TemplateResponse("ActualizarMovimiento.html", {"request": request})

@app.get("/eliminar", response_class=HTMLResponse)
def index_eliminar(request: Request):
    return templates.TemplateResponse("EliminarMovimiento.html", {"request": request})

# Crear un nuevo movimiento
@app.post("/create")
async def create_movement(
    id: int = Form(...),
    type: str = Form(...),
    amount: float = Form(...),
    controller: UniversalController = Depends(get_controller),
):
    try:
        new_movement = MovementCreate(id=id, type=type, amount=amount)
        controller.add(new_movement)
        return {
            "operation": "create",
            "success": True,
            "data": MovementOut(id=new_movement.id, type=new_movement.type, amount=new_movement.amount).dict(),
            "message": "Movement created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

# Actualizar un movimiento
@app.post("/update")
async def update_movement(
    id: int = Form(...),
    type: str = Form(...),
    amount: float = Form(...),
    controller: UniversalController = Depends(get_controller),
):
    try:
        existing = controller.get_by_id(MovementOut, id)
        if not existing:
            raise HTTPException(404, detail="Movement not found")

        updated_movement = MovementCreate(id=id, type=type, amount=existing.amount)
        controller.update(updated_movement)

        return {
            "operation": "update",
            "success": True,
            "data": MovementOut(id=updated_movement.id, type=updated_movement.type, amount=updated_movement.amount).dict(),
            "message": f"Movement {id} updated successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

# Eliminar un movimiento
@app.post("/delete")
async def delete_movement(
    id: int = Form(...),
    controller: UniversalController = Depends(get_controller),
):
    try:
        existing = controller.get_by_id(MovementOut, id)
        if not existing:
            raise HTTPException(404, detail="Movement not found")

        controller.delete(existing)

        return {
            "operation": "delete",
            "success": True,
            "message": f"Movement {id} deleted successfully"
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))
