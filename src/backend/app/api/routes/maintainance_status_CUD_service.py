from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.maintainance_status import MaintainanceStatusCreate, MaintainanceStatusOut
from backend.app.logic.universal_controller_sql import UniversalController
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
@app.get("/maintainance_status/crear", response_class=HTMLResponse, tags=["maintenance"])
def show_create_form(request: Request):
    return templates.TemplateResponse("CrearEstadoMantenimiento.html", {"request": request})

@app.get("/maintainance_status/actualizar", response_class=HTMLResponse, tags=["maintenance"])
def show_update_form(request: Request):
    return templates.TemplateResponse("ActualizarEstadoMantenimiento.html", {"request": request})

@app.get("/maintainance_status/eliminar", response_class=HTMLResponse, tags=["maintenance"])
def show_delete_form(request: Request):
    return templates.TemplateResponse("EliminarEstadoMantenimiento.html", {"request": request})

# Endpoints POST para operaciones
@app.post("/maintainance_status/create", response_model=MaintainanceStatusOut, tags=["maintenance"])
async def create_status(
    id: int = Form(...),
    unit: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
):
    try:
        new_status = MaintainanceStatusCreate(
            id=id,
            unit=unit,
            type=type,
            status=status
        )
        result = controller.add(new_status)
        return MaintainanceStatusOut(
            id=result.id,
            unit=result.unit,
            type=result.type,
            status=result.status
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Error interno del servidor: {str(e)}")

@app.post("/maintainance_status/update", response_model=MaintainanceStatusOut, tags=["maintenance"])
async def update_status(
    id: int = Form(...),
    unit: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
):
    try:
        existing = controller.get_by_id(MaintainanceStatusOut, id)
        if not existing:
            raise HTTPException(404, detail="Registro no encontrado")
        
        updated_status = MaintainanceStatusCreate(
            id=id,
            unit=unit,
            type=type,
            status=status
        )
        result = controller.update(updated_status)
        return MaintainanceStatusOut(
            id=result.id,
            unit=result.unit,
            type=result.type,
            status=result.status
        )
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/maintainance_status/delete", tags=["maintenance"])
async def delete_status(id: int = Form(...)):
    try:
        existing = controller.get_by_id(MaintainanceStatusOut, id)
        if not existing:
            raise HTTPException(404, detail="Registro no encontrado")
        
        controller.delete(existing)
        return {"message": f"Estado {id} eliminado correctamente"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)