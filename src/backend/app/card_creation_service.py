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
    return templates.TemplateResponse("CrearTarjeta.html", {"request": request})

@app.post("/CardCreation/add_tarjeta")
async def add_tarjeta(
    request: Request,
    id: str = Form(...),
    tipo: str = Form(...),
    saldo: float = 0
):
    card_temp = Card(id, tipo, saldo)
    return st_object.add(card_temp)
if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)