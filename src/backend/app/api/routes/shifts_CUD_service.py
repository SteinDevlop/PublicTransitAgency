from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.shift import ShiftCreate, ShiftOut
from backend.app.logic.universal_controller_sql import UniversalController
from datetime import datetime
import uvicorn

app = FastAPI()
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

# Endpoints GET para formularios HTML
@app.get("/shift/crear", response_class=HTMLResponse, tags=["shifts"])
def show_create_form(request: Request):
    return templates.TemplateResponse("CrearTurno.html", {"request": request})

@app.get("/shift/actualizar", response_class=HTMLResponse, tags=["shifts"])
def show_update_form(request: Request):
    return templates.TemplateResponse("ActualizarTurno.html", {"request": request})

@app.get("/shift/eliminar", response_class=HTMLResponse, tags=["shifts"])
def show_delete_form(request: Request):
    return templates.TemplateResponse("EliminarTurno.html", {"request": request})

# Endpoints POST para operaciones
@app.post("/shift/create", response_model=ShiftOut, tags=["shifts"])
async def create_shift(
    shift_id: str = Form(...),
    unit: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    driver: str = Form(...),
    schedule: str = Form(...)
):
    try:
        new_shift = ShiftCreate(
            shift_id=shift_id,
            unit=unit,
            start_time=datetime.fromisoformat(start_time),
            end_time=datetime.fromisoformat(end_time),
            driver=driver,
            schedule=schedule
        )
        result = controller.add(new_shift)
        return ShiftOut(**result.__dict__)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Error interno del servidor: {str(e)}")

@app.post("/shift/update", response_model=ShiftOut, tags=["shifts"])
async def update_shift(
    shift_id: str = Form(...),
    unit: str = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    driver: str = Form(...),
    schedule: str = Form(...)
):
    try:
        existing = controller.get_by_id(ShiftOut, shift_id)
        if not existing:
            raise HTTPException(404, detail="Turno no encontrado")

        updated_shift = ShiftCreate(
            shift_id=shift_id,
            unit=unit,
            start_time=datetime.fromisoformat(start_time),
            end_time=datetime.fromisoformat(end_time),
            driver=driver,
            schedule=schedule
        )
        result = controller.update(updated_shift)
        return ShiftOut(**result.__dict__)
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@app.post("/shift/delete", tags=["shifts"])
async def delete_shift(shift_id: str = Form(...)):
    try:
        existing = controller.get_by_id(ShiftOut, shift_id)
        if not existing:
            raise HTTPException(404, detail="Turno no encontrado")
        
        controller.delete(existing)
        return {"message": f"Turno {shift_id} eliminado correctamente"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=True)
