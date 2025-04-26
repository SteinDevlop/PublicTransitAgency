from fastapi import FastAPI, Form, Request, status, Query,APIRouter
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from backend.app.models.card import CardCreate, CardOut
from backend.app.logic.universal_controller_sql import UniversalController

app = APIRouter(prefix="/card", tags=["card"])
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
    return templates.TemplateResponse("ConsultarTarjeta.html", {"request": request})

@app.get("/tarjetas")
async def get_tarjetas():
    return controller.read_all(CardOut)

@app.get("/tarjeta", response_class=HTMLResponse)
def tarjeta(request: Request, id: int = Query(...)):
    unit_tarjeta = controller.get_by_id(CardOut, id)
    if unit_tarjeta:
        return templates.TemplateResponse("tarjeta.html", {
            "request": request,
            "id": unit_tarjeta.id,
            "tipo": unit_tarjeta.tipo,
            "saldo": unit_tarjeta.balance
        })
    return templates.TemplateResponse("tarjeta.html", {
        "request": request,
        "id": "None",
        "tipo": "None",
        "saldo": "None"
    })
