#rol_user_cud_service.py
# This module provides CRUD operations for the RolUser model using FastAPI.
# It includes routes for creating, updating, and deleting roles of users.

from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.rol_user import RolUserCreate, RolUserOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/roluser", tags=["Rol User"])
templates = Jinja2Templates(directory="src/backend/app/templates")  # Set up the template directory

def get_controller():
    return UniversalController()

# Route to create a role of user
@app.get("/crear", response_class=HTMLResponse)
def crear_rol_user(request: Request):
    """
    Displays the form to create a new role of user.
    """
    return templates.TemplateResponse("CrearRolUsuario.html", {"request": request})

# Route to delete a role of user
@app.get("/eliminar", response_class=HTMLResponse)
def eliminar_rol_user(request: Request):
    """
    Displays the form to delete a new role of user.
    """
    return templates.TemplateResponse("EliminarRolUsuario.html", {"request": request})

# Route to update a role of user
@app.get("/actualizar", response_class=HTMLResponse)
def actualizar_rol_user(request: Request):
    """
    Displays the form to update an existing role of user.
    """
    return templates.TemplateResponse("ActualizarRolUsuario.html", {"request": request})

# Route to add a new role of user
@app.post("/create")
async def add_roluser(
    id: int = Form(...),
    type: str = Form(...),
    controller: UniversalController = Depends(get_controller),
):
    """
    Creates a new role of user with the provided ID and type.
    The controller is used to add the role of user to the database.
    """
    try:
        new_roluser = RolUserCreate(id=id, type=type)
        
        # Add the new role of user using the controller
        result = controller.add(new_roluser)
        
        return {
            "operation": "create",
            "success": True,
            "data": RolUserCreate(id=new_roluser.id, type=new_roluser.type).model_dump(),
            "message": "Role User created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))  # Bad request if validation fails
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")  # General server error

# Route to update an existing role of user
@app.post("/update")
async def update_roluser(
    id: int = Form(...),
    type: str = Form(...),
    controller: UniversalController = Depends(get_controller)
):
    """
    Updates an existing role of user by its ID and new type.
    If the role of user does not exist, a 404 error is raised.
    """
    try:
        # Look for the existing role of user to update
        existing = controller.get_by_id(RolUserOut, id)
        if existing is None:
            raise HTTPException(404, detail="Not found")
        
        # Create a new instance with the updated data
        updated_roluser = RolUserCreate(id=id, type=type)
        
        # Update the role of user using the controller
        result = controller.update(updated_roluser)
        
        return {
            "operation": "update",
            "success": True,
            "data": RolUserOut(id=updated_roluser.id, type=updated_roluser.type).model_dump(),
            "message": f"Role User updated successfully"
        }
    except HTTPException as e:
        raise e  # <-- Permitir que se propague tal como está
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

# Route to delete a role of user
@app.post("/delete")
async def delete_roluser(id: int = Form(...), controller: UniversalController = Depends(get_controller)):
    """
    Deletes an existing role of user by its ID.
    If the role of user does not exist, a 404 error is raised.
    """
    try:
        # Look for the role of user to delete
        existing = controller.get_by_id(RolUserOut, id)
        if not existing:
            raise HTTPException(404, detail="Not found")
        
        # Delete the role of user using the controller
        controller.delete(existing)
        
        return {
            "operation": "delete",
            "success": True,
            "message": f"Role User deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))  # General server error



