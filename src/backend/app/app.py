from fastapi import FastAPI, Form, Request, status, Query
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from logic.card import Card
from logic.card_controller import CardController

app = FastAPI()
st_object = CardController()

# Descomenta esta línea si estás sirviendo archivos estáticos
# app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    print("Request for index page received")
    return templates.TemplateResponse("CrearTarjeta.html", {"request": request})

@app.get('/consultar', response_class=HTMLResponse)
def consultar(request: Request):
    print("Request for index page received")
    return templates.TemplateResponse("ConsultarTarjeta.html", {"request": request})
@app.get("/tarjetas")
async def get_tarjetas():
    return st_object.show()
@app.get("/tarjeta")
def tarjeta(request:Request, id: str):
    unitTarjeta=st_object.get_by_id(id)
    if unitTarjeta != None:
        return templates.TemplateResponse("tarjeta.html",{"request":request,"id": unitTarjeta["idn"],"tipo": unitTarjeta["tipo"],"saldo": unitTarjeta["saldo"]})
    if unitTarjeta is None:
        return templates.TemplateResponse("tarjeta.html",{"request":request,"id": "None","tipo": "None","saldo": "None"})
@app.post("/add_tarjeta")
async def add_tarjeta(
    request: Request,
    id: str = Form(...),
    tipo: str = Form(...),
    saldo: float = Form(...)
):
    card_temp = Card(id, tipo, saldo)
    print(card_temp)
    return st_object.add(card_temp)

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)