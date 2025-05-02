from fastapi import FastAPI, Form, HTTPException, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.maintainance_status import MaintainanceStatusCreate, MaintainanceStatusOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/maintainance_status", tags=["maintainance_status"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get("/crear", response_class=HTMLResponse)
def index_create(request: Request):
    """Displays the form to create a new maintainance status."""
    return templates.TemplateResponse("CrearEstadoMantenimiento.html", {"request": request})  # Crear HTML

@app.get("/actualizar", response_class=HTMLResponse)
def index_update(request: Request):
    """Displays the form to update an existing maintainance status."""
    return templates.TemplateResponse("ActualizarEstadoMantenimiento.html", {"request": request}) # Crear HTML

@app.get("/eliminar", response_class=HTMLResponse)
def index_delete(request: Request):
    """Displays the form to delete an existing maintainance status."""
    return templates.TemplateResponse("EliminarEstadoMantenimiento.html", {"request": request}) # Crear HTML

@app.post("/create")
async def create_maintainance_status(
    TipoEstado: str = Form(...),
    UnidadTransporte: str = Form(None),  # Permite valores nulos
    Status: str = Form(...)
):
    """Creates a new maintainance status."""
    try:
        new_status = MaintainanceStatusCreate(
            TipoEstado=TipoEstado,
            UnidadTransporte=UnidadTransporte,
            Status=Status
        )
        result = controller.add(new_status)
        return {
            "operation": "create",
            "success": True,
            "data": MaintainanceStatusOut(
                ID=result.ID, # Asegurarse de que el ID se devuelve correctamente
                TipoEstado=result.TipoEstado,
                UnidadTransporte=result.UnidadTransporte,
                Status=result.Status
            ).dict(),
            "message": "Maintainance status created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@app.post("/update")
async def update_maintainance_status(
    ID: int = Form(...),  # Usar "ID"
    TipoEstado: str = Form(...),
    UnidadTransporte: str = Form(None), # Permitir nulos
    Status: str = Form(...)
):
    """Updates an existing maintainance status."""
    try:
        existing_status = controller.get_by_id(MaintainanceStatusOut, ID) # Usar MaintainanceStatusOut
        if not existing_status:
            raise HTTPException(404, detail="Maintainance status not found")

        updated_status = MaintainanceStatusCreate( # Usar MaintainanceStatusCreate para la validacion
            ID=ID,
            TipoEstado=TipoEstado,
            UnidadTransporte=UnidadTransporte,
            Status=Status
        )
        result = controller.update(updated_status) # Pasar el objeto Pydantic
        return {
            "operation": "update",
            "success": True,
            "data": MaintainanceStatusOut( # Usar MaintainanceStatusOut para la respuesta
                ID=result.ID,
                TipoEstado=result.TipoEstado,
                UnidadTransporte=result.UnidadTransporte,
                Status=result.Status
            ).dict(),
            "message": f"Maintainance status {ID} updated successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@app.post("/delete")
async def delete_maintainance_status(ID: int = Form(...)): # Usar "ID"
    """Deletes an existing maintainance status."""
    try:
        existing_status = controller.get_by_id(MaintainanceStatusOut, ID) # Usar MaintainanceStatusOut
        if not existing_status:
            raise HTTPException(404, detail="Maintainance status not found")
        controller.delete(existing_status) 
        return {
            "operation": "delete",
            "success": True,
            "message": f"Maintainance status {ID} deleted successfully"
        }
    except HTTPException as e:
        raise e # Dejar pasar las excepciones HTTP
    except Exception as e:
        raise HTTPException(500, detail=str(e))