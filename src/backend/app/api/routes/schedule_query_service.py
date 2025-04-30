from fastapi import FastAPI, HTTPException, Request, Query, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from backend.app.models.schedule import ScheduleOut
from logic.universal_controller_sql import UniversalController
import uvicorn

# Initialize the FastAPI router for the "schedule" functionality
app = APIRouter(prefix="/schedules", tags=["horarios"])

controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Endpoint para la página de consulta principal (HTML)
@app.get("/consultar", response_class=HTMLResponse)
async def consultar_horarios_html(request: Request):
    """Renderiza la página para consultar horarios."""
    return templates.TemplateResponse("ConsultarHorarios", {"request": request})

# Endpoint para obtener todos los horarios (HTML)
@app.get("", response_class=HTMLResponse)
async def listar_horarios_html(request: Request):
    """Lista todos los horarios en formato HTML."""
    dummy = ScheduleOut.get_empty_instance()
    horarios = controller.read_all(dummy)
    return templates.TemplateResponse("ListarHorarios", {"request": request, "horarios": horarios})

# Endpoint para obtener todos los horarios (JSON)
@app.get("/json")
async def listar_horarios_json():
    """Lista todos los horarios en formato JSON."""
    dummy = ScheduleOut.get_empty_instance()
    horarios = controller.read_all(dummy)
    return JSONResponse(content={"data": [horario.dict() for horario in horarios]})

# Endpoint para obtener un horario por ID (HTML)
@app.get("/{schedule_id}", response_class=HTMLResponse)
async def obtener_horario_html(request: Request, schedule_id: str = Query(...)):
    """Obtiene un horario por su ID y lo muestra en HTML."""
    horario = controller.get_by_id(ScheduleOut, schedule_id)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return templates.TemplateResponse("DetalleHorario", {"request": request, "horario": horario})

# Endpoint para obtener un horario por ID (JSON)
@app.get("/{schedule_id}/json")
async def obtener_horario_json(schedule_id: str = Query(...)):
    """Obtiene un horario por su ID en formato JSON."""
    horario = controller.get_by_id(ScheduleOut, schedule_id)
    if not horario:
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return JSONResponse(content={"data": horario.dict()})

if __name__ == "__main__":
    app_main = FastAPI(
        title="Query Service - Horarios",
        description="Microservicio para consulta de horarios de transporte",
        version="1.0.0"
    )
    app_main.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app_main.include_router(app)
    uvicorn.run(app_main, host="0.0.0.0", port=8003, reload=True)