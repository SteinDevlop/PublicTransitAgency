from fastapi import FastAPI, Form, Request, status, Query,APIRouter
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.app.models.user import UserCreate, UserOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/user", tags=["user"])
controller = UniversalController()  # Asegúrate de tener el controlador correspondiente
# Descomenta esta línea si estás sirviendo archivos estáticos
# app.mount("/static", StaticFiles(directory="static"), name="static")

controller = UniversalController()

# Descomenta esta línea si vas a servir archivos estáticos (CSS, JS, imágenes)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Plantillas HTML
templates = Jinja2Templates(directory="src/backend/app/templates")

@app.get('/consultar', response_class=HTMLResponse)
def consultar(request: Request):
    return templates.TemplateResponse("ConsultarUsuario.html", {"request": request})

@app.get("/usuarios")
async def get_usuarios():
    return controller.read_all(UserOut)

@app.get("/usuario", response_class=HTMLResponse)
def tarjeta(request: Request, id: int = Query(...)):
    unit_usuario = controller.get_by_id(UserOut, id)
    if unit_usuario:
        return templates.TemplateResponse("usuario.html", {
            "request": request,
            "id": unit_usuario.id,
            "identification":unit_usuario.identification,
            "name":unit_usuario.name,
            "lastname":unit_usuario.lastname,
            "email":unit_usuario.email,
            "password":unit_usuario.password,
            "idtype_user":unit_usuario.idtype_user,
            "idturn":unit_usuario.idturn
        })
    return templates.TemplateResponse("usuario.html", {
        "request": request,
            "id": "none",
            "identification":"none",
            "name":"none",
            "lastname":"none",
            "email":"none",
            "password":"none",
            "idtype_user":"none",
            "idturn":"none"
    })
