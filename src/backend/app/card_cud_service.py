from fastapi import FastAPI, Form, Request, status, Query, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from logic.card import Card
from logic.card_controller import CardController

app = FastAPI()
st_object = CardController()

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

@app.get("/crear", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("CrearTarjeta.html", {"request": request})
@app.get("/actualizar", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("ActualizarTarjeta.html", {"request": request})
@app.get("/eliminar", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("EliminarTarjeta.html", {"request": request})
@app.post("/CardCreation/add_tarjeta")
async def add_tarjeta(
    request: Request,
    id: str = Form(...),
    tipo: str = Form(...),
    saldo: float = 0
):
    card_temp = Card(id, tipo, saldo)
    return st_object.add(card_temp)

@app.post("/CardCreation/update_tarjeta/")
async def update_tarjeta(
    card_id: str,
    tipo: str = Form(...),
    saldo: float = Form(...)
):
    card_temp = Card(card_id, tipo, saldo)
    updated = st_object.update(card_temp)
    if not updated:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return {"message": "Tarjeta actualizada correctamente"}

@app.post("/CardCreation/delete_tarjeta/")
async def delete_tarjeta(card_id: str):
    deleted = st_object.delete(card_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tarjeta no encontrada")
    return {"message": "Tarjeta eliminada correctamente"}

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)
