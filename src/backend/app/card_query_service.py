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
@app.get('/CardQuery/consultar', response_class=HTMLResponse)
def consultar(request: Request):
    return templates.TemplateResponse("ConsultarTarjeta.html", {"request": request})

@app.get("/CardQuery/tarjetas")
async def get_tarjetas():
    return st_object.show()

@app.get("/CardQuery/tarjeta")
def tarjeta(request:Request, id: str):
    unitTarjeta = st_object.get_by_id(id)
    if unitTarjeta:
        return templates.TemplateResponse("tarjeta.html", {
            "request": request,
            "id": unitTarjeta["idn"],
            "tipo": unitTarjeta["tipo"],
            "saldo": unitTarjeta["saldo"]
        })
    return templates.TemplateResponse("tarjeta.html", {
        "request": request,
        "id": "None",
        "tipo": "None",
        "saldo": "None"
    })
if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)