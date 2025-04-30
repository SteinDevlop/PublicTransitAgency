from fastapi import FastAPI, APIRouter, Form, HTTPException,APIRouter,Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from backend.app.models.user import UserCreate, UserOut  # Asegúrate de que tus modelos estén en este archivo
from  backend.app.logic.universal_controller_sql import UniversalController 

app = APIRouter(prefix="/user", tags=["user"])
templates = Jinja2Templates(directory="src/backend/app/templates")

def get_controller():
    """
    Dependency to get the controller instance.
    """
    return UniversalController()

@app.get("/crear", response_class=HTMLResponse)
def index(request: Request):
    """
    Displays the form to create a new user.
    """
    return templates.TemplateResponse("CrearUsuario.html", {"request": request})
@app.get("/actualizar", response_class=HTMLResponse)
def index(request: Request):
    """
    Displays the form to update an existing user.
    """
    return templates.TemplateResponse("ActualizarUsuario.html", {"request": request})
@app.get("/eliminar", response_class=HTMLResponse)
def index(request: Request):
    """
    Displays the form to delete an existing user."""
    return templates.TemplateResponse("EliminarUsuario.html", {"request": request})
@app.post("/create")
async def create_user(
    id: int = Form(...),
    identification: int = Form(...),
    name: str = Form(...),
    lastname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    idtype_user: int = Form(...),
    idturn: int = Form(...),
    controller: UniversalController = Depends(get_controller)
):
    try:
        new_user = UserCreate(
            id=id,
            identification=identification,
            name=name,
            lastname=lastname,
            email=email,
            password=password,
            idtype_user=idtype_user,
            idturn=idturn
        )
        # AQUÍ: NO LLAMES to_dict()
        result = controller.add(new_user)
        
        return {
            "operation": "create",
            "success": True,
            "data": UserOut(id=new_user.id, identification=new_user.identification, name=new_user.name,
                            lastname=new_user.lastname, email=new_user.email,password=new_user.password,
                            idtype_user=new_user.idtype_user, idturn=new_user.idturn).model_dump(),
            "message": "User created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"An error occurred: {str(e)}")

@app.post("/update")
async def update_user(
    id: int = Form(...),
    identification: int = Form(...),
    name: str = Form(...),
    lastname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    idtype_user: int = Form(...),
    idturn: int = Form(...),
    controller: UniversalController = Depends(get_controller)
):
    try:
        # Buscar el usuario existente para actualización
        existing = controller.get_by_id(UserOut, id)  # Aquí usamos UserOut para buscar la usuario
        if existing is None:
            raise HTTPException(404, detail="User not found")
        
        # Crear una instancia del modelo UserCreate para validar los datos de actualización
        updated_user = UserCreate(
            id=id,
            identification=identification,
            name=name,
            lastname=lastname,
            email=email,
            password=password,
            idtype_user=idtype_user,
            idturn=idturn
        )
        # Usamos el controlador para actualizar la usuario (convertimos el modelo a dict)
        result = controller.update(updated_user)
        
        # Devolvemos la respuesta con la usuario actualizada utilizando UserOut
        return {
            "operation": "update",
            "success": True,
            "data": UserOut(id=updated_user.id, identification=updated_user.identification, name=updated_user.name,
                            lastname=updated_user.lastname, email=updated_user.email,password=updated_user.password,
                            idtype_user=updated_user.idtype_user, idturn=updated_user.idturn).model_dump(),
            "message": f"User updated successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/delete")
async def delete_user(id: int = Form(...), controller: UniversalController = Depends(get_controller)):
    try:
        # Buscar la usuario para eliminar
        existing = controller.get_by_id(UserOut, id)  # Usamos UserOut para buscar la usuario
        if existing is None:
            raise HTTPException(404, detail="User not found")
        
        # Usamos el controlador para eliminar la usuario
        controller.delete(existing)
        
        return {
            "operation": "delete",
            "success": True,
            "message": f"User deleted successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, detail=str(e))  # General server error