#type_transport_cud_service.py
# This file contains the CRUD operations for TypeTransport using FastAPI.
# It includes routes for creating, updating, and deleting TypeTransport records.

from fastapi import APIRouter, Form, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.type_transport import TypeTransportCreate, TypeTransportOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/typetransport", tags=["Type Transport"])
templates = Jinja2Templates(directory="src/backend/app/templates")  # Set up the template directory

def get_controller():
    """
    Returns an instance of the UniversalController for database operations.
    """
    return UniversalController()

# Route to create a type of transport
@app.get("/crear", response_class=HTMLResponse)
def crear_tipo_transporte(request: Request):
    """
    Displays the form to create a new type of transport.
    """
    return templates.TemplateResponse("CrearTipoTransporte.html", {"request": request})

# Route to delete a type of transport
@app.get("/eliminar", response_class=HTMLResponse)
def eliminar_tipo_transporte(request: Request):
    """
    Displays the form to delete a type of transport.
    """
    return templates.TemplateResponse("EliminarTipoTransporte.html", {"request": request})

# Route to update a type of transport
@app.get("/actualizar", response_class=HTMLResponse)
def actualizar_tipo_transporte(request: Request):
    """
    Displays the form to update an existing type of transport.
    """
    return templates.TemplateResponse("ActualizarTipoTransporte.html", {"request": request})

# Route to add a new type of transport
@app.post("/create")
async def add_typetransport(
    id: int = Form(...),
    type: str = Form(...),
    controller: UniversalController = Depends(get_controller)
):
    """
    Creates a new type of transport with the provided ID and type.
    The controller is used to add the type of transport to the database.
    """
    try:
        new_typetransport = TypeTransportCreate(id=id, type=type)
        
        # Add the new type of transport using the controller
        result = controller.add(new_typetransport)
        
        return {
            "operation": "create",
            "success": True,
            "data": TypeTransportOut(id=new_typetransport.id, type=new_typetransport.type).model_dump(),
            "message": "Transport type created successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))  # General server error

# Route to update an existing type of transport
@app.post("/update")
async def update_typetransport(
    id: int = Form(...),
    type: str = Form(...),
    controller: UniversalController = Depends(get_controller)
):
    """
    Updates an existing type of transport by its ID and new type.
    If the type of transport does not exist, a 404 error is raised.
    """
    try:
        # Look for the existing type of transport to update
        existing = controller.get_by_id(TypeTransportOut, id)
        if existing is None:
            raise HTTPException(404, detail="Transport type not found")
        
        # Create a new instance with the updated data
        updated_typetransport = TypeTransportCreate(id=id, type=type)
        
        # Update the type of transport using the controller
        result = controller.update(updated_typetransport)
        
        return {
            "operation": "update",
            "success": True,
            "data": TypeTransportOut(id=updated_typetransport.id, type=updated_typetransport.type).model_dump(),
            "message": f"Transport type updated successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))  # General server error

# Route to delete a type of transport
@app.post("/delete")
async def delete_typetransport(id: int = Form(...), controller: UniversalController = Depends(get_controller)):
    """
    Deletes an existing type transport by its ID.
    If the type of transport does not exist, a 404 error is raised.
    """
    try:
        # Look for the type of transport to delete
        existing = controller.get_by_id(TypeTransportOut, id)
        if existing is None:
            raise HTTPException(404, detail="Transport type not found")
        
        # Delete the type of transport using the controller
        controller.delete(existing)
        
        return {
            "operation": "delete",
            "success": True,
            "message": f"Transport type deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))  # General server error
