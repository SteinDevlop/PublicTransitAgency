from fastapi import FastAPI, Form, HTTPException, APIRouter, Request
from fastapi.templating import Jinja2Templates
import datetime
from fastapi.responses import HTMLResponse

from backend.app.models.shift import ShiftCreate, ShiftOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/shifts", tags=["shifts"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/crear", response_class=HTMLResponse)
def index_create(request: Request):
    return templates.TemplateResponse("CrearTurno.html", {"request": request})

@app.get("/actualizar", response_class=HTMLResponse)
def index_update(request: Request):
    return templates.TemplateResponse("ActualizarTurno.html", {"request": request})

@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(request: Request):
    return templates.TemplateResponse("EliminarTurno.html", {"request": request})

@app.post("/create")
async def create_shift(
    shift_id: str = Form(...),
    unit: str = Form(...),
    start_time: datetime.datetime = Form(...),
    end_time: datetime.datetime = Form(...),
    driver: str = Form(...),
    schedule: str = Form(...)
):
    try:
        new_shift = ShiftCreate(
            shift_id=shift_id,
            unit_id=unit,
            start_time=start_time,
            end_time=end_time,
            driver_id=driver,
            schedule_id=schedule
        )
        result = controller.add(new_shift)
        return {"operation": "create", "success": True, "data": ShiftOut(**result.to_dict()).dict(), "message": "Shift created successfully"}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@app.post("/update/{shift_id}")
async def update_shift(
    shift_id: str,
    unit: str = Form(None),
    start_time: datetime.datetime = Form(None),
    end_time: datetime.datetime = Form(None),
    driver: str = Form(None),
    schedule: str = Form(None)
):
    try:
        existing_shift = controller.get_by_id(ShiftOut, shift_id)
        if not existing_shift:
            raise HTTPException(404, detail="Shift not found")

        update_data = ShiftCreate(
            shift_id=shift_id,  # ID from path, ensure consistency
            unit_id=unit if unit is not None else existing_shift.unit_id,
            start_time=start_time if start_time is not None else existing_shift.start_time,
            end_time=end_time if end_time is not None else existing_shift.end_time,
            driver_id=driver if driver is not None else existing_shift.driver_id,
            schedule_id=schedule if schedule is not None else existing_shift.schedule_id
        )
        result = controller.update(update_data)
        return {"operation": "update", "success": True, "data": ShiftOut(**result.to_dict()).dict(), "message": f"Shift {shift_id} updated successfully"}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=str(e))

@app.post("/delete/{shift_id}")
async def delete_shift(shift_id: str):
    try:
        existing_shift = controller.get_by_id(ShiftOut, shift_id)
        if not existing_shift:
            raise HTTPException(404, detail="Shift not found")
        controller.delete(existing_shift)
        return {"operation": "delete", "success": True, "message": f"Shift {shift_id} deleted successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=str(e))
