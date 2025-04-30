from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.schedule import ScheduleCreate, ScheduleOut
from datetime import datetime
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn
app = FastAPI()
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints GET para formularios HTML
@app.get("/schedule/crear", response_class=HTMLResponse, tags=["schedule"])
def show_create_form(request: Request):
    return templates.TemplateResponse("CrearHorario.html", {"request": request})

@app.get("/schedule/actualizar", response_class=HTMLResponse, tags=["schedule"])
def show_update_form(request: Request):
    return templates.TemplateResponse("ActualizarHorario.html", {"request": request})

@app.get("/schedule/eliminar", response_class=HTMLResponse, tags=["schedule"])
def show_delete_form(request: Request):
    return templates.TemplateResponse("EliminarHorario.html", {"request": request})

# Endpoints POST para operaciones
@app.post("/schedule/create", response_model=ScheduleOut, tags=["schedule"])
async def create_schedule(
    schedule_id: str = Form(...),
    arrival_date: str = Form(...),
    departure_date: str = Form(...),
    route: str = Form(...),
):
    try:
        schedule = ScheduleCreate(
            schedule_id=schedule_id,
            arrival_date=datetime.fromisoformat(arrival_date),
            departure_date=datetime.fromisoformat(departure_date),
            route=route,
        )
        result = controller.add(schedule.to_dict())
        return ScheduleOut(
            schedule_id=result.schedule_id,
            arrival_date=result.arrival_date,
            departure_date=result.departure_date,
            route=result.route,
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Error interno del servidor: {str(e)}")

@app.post("/schedule/update", response_model=ScheduleOut, tags=["schedule"])
async def update_schedule(
    schedule_id: str = Form(...),
    arrival_date: str = Form(...),
    departure_date: str = Form(...),
    route: str = Form(...),
):
    try:
        existing = controller.get_by_id(ScheduleOut, schedule_id)
        if not existing:
            raise HTTPException(404, detail="Horario no encontrado")
        
        updated_schedule = ScheduleCreate(
            schedule_id=schedule_id,
            arrival_date=datetime.fromisoformat(arrival_date),
            departure_date=datetime.fromisoformat(departure_date),
            route=route,
        )
        result = controller.update(updated_schedule.to_dict())
        return ScheduleOut(
            schedule_id=result.schedule_id,
            arrival_date=result.arrival_date,
            departure_date=result.departure_date,
            route=result.route,
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/schedule/delete", tags=["schedule"])
async def delete_schedule(schedule_id: str = Form(...)):
    try:
        existing = controller.get_by_id(ScheduleOut, schedule_id)
        if not existing:
            raise HTTPException(404, detail="Horario no encontrado")
        
        controller.delete(existing)
        return {"message": f"Horario {schedule_id} eliminado correctamente"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8003, reload=True)
