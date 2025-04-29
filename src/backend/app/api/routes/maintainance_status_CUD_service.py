from fastapi import FastAPI, Form, HTTPException, APIRouter, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from backend.app.models.maintainance_status import MaintainanceStatusCreate, MaintainanceStatusOut
from backend.app.logic.universal_controller_sql import UniversalController 
from backend.app.core.auth import get_current_user
import uvicorn

app = APIRouter(prefix="/maintainance_status", tags=["maintainance_status"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route to display the "Create Status" form
@app.get("/crear", response_class=HTMLResponse)
def index_create(request: Request):
    return templates.TemplateResponse("CrearEstadoMantenimiento.html", {"request": request})

# Route to display the "Update Status" form
@app.get("/actualizar", response_class=HTMLResponse)
def index_update(request: Request):
    return templates.TemplateResponse("ActualizarEstadoMantenimiento.html", {"request": request})

# Route to display the "Delete Status" form
@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(request: Request):
    return templates.TemplateResponse("EliminarEstadoMantenimiento.html", {"request": request})

# Route to create a new status
@app.post("/create")
async def create_status(
    request: Request,
    id: int = Form(...),
    unit: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    #user = Depends(get_current_user)
):
    try:
        new_status = MaintainanceStatusCreate(
            id=id,
            unit=unit,
            type=type,
            status=status
        )
        result = controller.add(new_status)
        
        if "text/html" in request.headers.get("Accept", ""):
            return templates.TemplateResponse("EstadoCreado.html", {
                "request": request,
                "id": result.id,
                "unit": result.unit,
                "type": result.type,
                "status": result.status
            })
            
        return {
            "operation": "create",
            "success": True,
            "data": MaintainanceStatusOut(
                id=new_status.id,
                unit=new_status.unit,
                type=new_status.type,
                status=new_status.status
            ).dict(),
            "message": "Estado de mantenimiento creado correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Error interno del servidor: {str(e)}")

# Route to update an existing status
@app.post("/update")
async def update_status(
    request: Request,
    id: int = Form(...),
    unit: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    #user = Depends(get_current_user)
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

        if "text/html" in request.headers.get("Accept", ""):
            return templates.TemplateResponse("EstadoActualizado.html", {
                "request": request,
                "id": result.id,
                "unit": result.unit,
                "type": result.type,
                "status": result.status
            })
        
        return {
            "operation": "update",
            "success": True,
            "data": MaintainanceStatusOut(
                id=updated_status.id,
                unit=updated_status.unit,
                type=updated_status.type,
                status=updated_status.status
            ).dict(),
            "message": f"Estado {id} actualizado correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

# Route to delete a status
@app.post("/delete")
async def delete_status(
    request: Request, 
    id: int = Form(...)
    #user = Depends(get_current_user)
):
    try:
        existing = controller.get_by_id(MaintainanceStatusOut, id)
        if not existing:
            raise HTTPException(404, detail="Registro no encontrado")
        
        controller.delete(existing)

        if "text/html" in request.headers.get("Accept", ""):
            return templates.TemplateResponse("EstadoEliminado.html", {
                "request": request,
                "id": id
            })
        
        return {
            "operation": "delete",
            "success": True,
            "message": f"Estado {id} eliminado correctamente"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=str(e))