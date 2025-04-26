from fastapi import FastAPI, Form, Request, status,Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from logic.type_card import TypeCard
from logic.universal_controller_sql import UniversalController

app = FastAPI()
controller = UniversalController()
templates = Jinja2Templates(directory="templates")

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Combined route with query parameter to load different pages
@app.get("/crear", response_class=HTMLResponse)
def crear_mantenimiento(request: Request):
    return templates.TemplateResponse("CrearTipoTarjeta.html", {"request": request})

@app.get("/eliminar", response_class=HTMLResponse)
def eliminar_mantenimiento(request: Request):
    return templates.TemplateResponse("EliminarTipoTarjeta.html", {"request": request})

@app.get("/actualizar", response_class=HTMLResponse)
def actualizar_mantenimiento(request: Request):
    return templates.TemplateResponse("ActualizarTipoTarjeta.html", {"request": request})
# Add mantainment
@app.post("/typecard/crear")
def add(
id: int = Form(...) , type: str = Form(...)
):
    typecard_temp = TypeCard(id, type)
    return controller.add(typecard_temp)

# Update mantainment
@app.post("/typecard/actualizar")
def update(
id: int = Form(...) , type: str = Form(...)
):
    typecard_temp = TypeCard(id, type)
    return controller.update(typecard_temp)

# Delete mantainment
@app.post("/typecard/eliminar")
def delete_mantainment(id: int = Form(...)):
    typecard_temp = TypeCard(id)
    controller.delete(typecard_temp)
    return controller.delete(typecard_temp)
