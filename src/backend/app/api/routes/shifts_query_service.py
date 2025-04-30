from fastapi import FastAPI, HTTPException, Request, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.shift import ShiftOut
from logic.universal_controller_sql import UniversalController
import uvicorn

# Initialize the FastAPI router for the "shift" functionality
app = APIRouter(prefix="/shifts", tags=["turnos"])

controller = UniversalController()
templates = Jinja2Templates(directory="templates")

# Endpoint para listar todos los turnos (HTML)
@app.get("", response_class=HTMLResponse)
async def listar_turnos_html(
    request: Request,
    skip: int = Query(0, description="Registros a saltar"),
    limit: int = Query(10, description="Límite de resultados")
):
    try:
        dummy = ShiftOut.get_empty_instance()
        shifts = controller.read_all(dummy)[skip:skip + limit]
        if not shifts:
            raise HTTPException(status_code=404, detail="No se encontraron turnos")
        return templates.TemplateResponse("listar_turnos.html", {"request": request, "turnos": shifts})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint para listar todos los turnos (JSON)
@app.get("/json")
async def listar_turnos_json(
    skip: int = Query(0, description="Registros a saltar"),
    limit: int = Query(10, description="Límite de resultados")
):
    try:
        dummy = ShiftOut.get_empty_instance()
        shifts = controller.read_all(dummy)[skip:skip + limit]
        if not shifts:
            raise HTTPException(status_code=404, detail="No se encontraron turnos")
        return JSONResponse(content={"data": [shift.dict() for shift in shifts]})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint para obtener un turno por ID (HTML)
@app.get("/{shift_id}", response_class=HTMLResponse)
async def obtener_turno_html(request: Request, shift_id: str):
    try:
        shift = controller.get_by_id(ShiftOut, shift_id)
        if not shift:
            raise HTTPException(status_code=404, detail="Turno no encontrado")
        return templates.TemplateResponse("detalle_turno.html", {"request": request, "turno": shift})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint para obtener un turno por ID (JSON)
@app.get("/{shift_id}/json")
async def obtener_turno_json(shift_id: str):
    try:
        shift = controller.get_by_id(ShiftOut, shift_id)
        if not shift:
            raise HTTPException(status_code=404, detail="Turno no encontrado")
        return JSONResponse(content={"data": shift.dict()})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint para obtener turnos por conductor (HTML)
@app.get("/conductor/{driver_id}", response_class=HTMLResponse)
async def obtener_turnos_por_conductor_html(
    request: Request,
    driver_id: str,
    skip: int = Query(0, description="Registros a saltar"),
    limit: int = Query(10, description="Límite de resultados")
):
    try:
        dummy = ShiftOut.get_empty_instance()
        all_shifts = controller.read_all(dummy)
        filtered = [s for s in all_shifts if s.driver_id == driver_id] # Asumiendo ShiftOut tiene driver_id
        paginated = filtered[skip:skip + limit]
        if not paginated:
            raise HTTPException(status_code=404, detail="No se encontraron turnos para este conductor")
        return templates.TemplateResponse("turnos_por_conductor.html", {"request": request, "turnos": paginated, "driver_id": driver_id})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint para obtener turnos por conductor (JSON)
@app.get("/conductor/{driver_id}/json")
async def obtener_turnos_por_conductor_json(
    driver_id: str,
    skip: int = Query(0, description="Registros a saltar"),
    limit: int = Query(10, description="Límite de resultados")
):
    try:
        dummy = ShiftOut.get_empty_instance()
        all_shifts = controller.read_all(dummy)
        filtered = [s for s in all_shifts if s.driver_id == driver_id] # Asumiendo ShiftOut tiene driver_id
        paginated = filtered[skip:skip + limit]
        if not paginated:
            raise HTTPException(status_code=404, detail="No se encontraron turnos para este conductor")
        return JSONResponse(content={"data": [shift.dict() for shift in paginated]})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint para obtener turnos por unidad (HTML)
@app.get("/unidad/{unit_id}", response_class=HTMLResponse)
async def obtener_turnos_por_unidad_html(
    request: Request,
    unit_id: str,
    skip: int = Query(0, description="Registros a saltar"),
    limit: int = Query(10, description="Límite de resultados")
):
    try:
        dummy = ShiftOut.get_empty_instance()
        all_shifts = controller.read_all(dummy)
        filtered = [s for s in all_shifts if s.unit_id == unit_id] # Asumiendo ShiftOut tiene unit_id
        paginated = filtered[skip:skip + limit]
        if not paginated:
            raise HTTPException(status_code=404, detail="No se encontraron turnos para esta unidad")
        return templates.TemplateResponse("turnos_por_unidad.html", {"request": request, "turnos": paginated, "unit_id": unit_id})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# Endpoint para obtener turnos por unidad (JSON)
@app.get("/unidad/{unit_id}/json")
async def obtener_turnos_por_unidad_json(
    unit_id: str,
    skip: int = Query(0, description="Registros a saltar"),
    limit: int = Query(10, description="Límite de resultados")
):
    try:
        dummy = ShiftOut.get_empty_instance()
        all_shifts = controller.read_all(dummy)
        filtered = [s for s in all_shifts if s.unit_id == unit_id] # Asumiendo ShiftOut tiene unit_id
        paginated = filtered[skip:skip + limit]
        if not paginated:
            raise HTTPException(status_code=404, detail="No se encontraron turnos para esta unidad")
        return JSONResponse(content={"data": [shift.dict() for shift in paginated]})
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    app_main = FastAPI()
    app_main.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    app_main.include_router(app)
    uvicorn.run(app_main, host="0.0.0.0", port=8006)