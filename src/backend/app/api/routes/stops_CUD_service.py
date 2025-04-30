from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.stops import StopCreate, StopOut
from logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()
templates = Jinja2Templates(directory="templates")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints GET para formularios HTML
@app.get("/stops/crear", response_class=HTMLResponse)
def show_create_form(request: Request):
    return templates.TemplateResponse("CrearStop.html", {"request": request})

@app.get("/stops/actualizar", response_class=HTMLResponse)
def show_update_form(request: Request):
    return templates.TemplateResponse("ActualizarStop.html", {"request": request})

@app.get("/stops/eliminar", response_class=HTMLResponse)
def show_delete_form(request: Request):
    return templates.TemplateResponse("EliminarStop.html", {"request": request})

# Endpoints POST para operaciones
@app.post("/stops/create", response_model=StopOut)
async def create_stop(
    stop_id: int = Form(...),
    stop_data: dict = Form(...),
):
    try:
        new_stop = StopCreate(
            stop_id=stop_id,
            stop_data=stop_data
        )
        result = controller.add(new_stop.to_dict())
        return StopOut(
            stop_id=result["stop_id"],
            stop_data=result["stop_data"]
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@app.post("/stops/update", response_model=StopOut)
async def update_stop(
    stop_id: int = Form(...),
    stop_data: dict = Form(...),
):
    try:
        existing = controller.get_by_id(StopOut, stop_id)
        if not existing:
            raise HTTPException(404, detail="Stop not found")
        
        updated_stop = StopCreate(
            stop_id=stop_id,
            stop_data=stop_data
        )
        result = controller.update(updated_stop.to_dict())
        return StopOut(
            stop_id=result["stop_id"],
            stop_data=result["stop_data"]
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/stops/delete")
async def delete_stop(stop_id: int = Form(...)):
    try:
        existing = controller.get_by_id(StopOut, stop_id)
        if not existing:
            raise HTTPException(404, detail="Stop not found")
        
        controller.delete(existing)
        return {"message": f"Stop {stop_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8007, reload=True)
