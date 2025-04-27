from fastapi import FastAPI, Form, HTTPException,APIRouter,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from backend.app.models.user import UserCreate, UserOut  # Asegúrate de que tus modelos estén en este archivo
from  backend.app.logic.universal_controller_sql import UniversalController 
import uvicorn

app = APIRouter(prefix="/user", tags=["User"])
controller = UniversalController()  # Asegúrate de tener el controlador correspondiente
templates = Jinja2Templates(directory="src/backend/app/templates")
@app.get("/crear", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("CrearUsuario.html", {"request": request})
@app.get("/actualizar", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("ActualizarUsuario.html", {"request": request})
@app.get("/eliminar", response_class=HTMLResponse)
def index(request: Request):
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
                            idtype_user=new_user.idtype_user, idturn=new_user.idturn).dict(),
            "message": "Usario creado correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Error interno del servidor: {str(e)}")

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
):
    try:
        # Buscar el usuario existente para actualización
        existing = controller.get_by_id(UserOut, id)  # Aquí usamos UserOut para buscar la usuario
        if not existing:
            raise HTTPException(404, detail="Usuario no encontrada")
        
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
            "data": UserOut(id=update_user.id, identification=update_user.identification, name=update_user.name,
                            lastname=update_user.lastname, email=update_user.email,password=update_user.password,
                            idtype_user=update_user.idtype_user, idturn=update_user.idturn).dict(),
            "message": f"Usuario {id} actualizado correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/delete")
async def delete_user(id: int = Form(...)):
    try:
        # Buscar la usuario para eliminar
        existing = controller.get_by_id(UserOut, id)  # Usamos UserOut para buscar la usuario
        if not existing:
            raise HTTPException(404, detail="Usuario no encontrado")
        
        # Usamos el controlador para eliminar la usuario
        controller.delete(existing)
        
        return {
            "operation": "delete",
            "success": True,
            "message": f"Usuario {id} eliminado correctamente"
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "app:app",  # Asegúrate de que tu archivo se llame app.py
        host="0.0.0.0",
        port=8001,  # Cambia el puerto si es necesario
        reload=True
    )
