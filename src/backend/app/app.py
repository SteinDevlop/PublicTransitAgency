from fastapi import FastAPI, Form, Request, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from logic.card import Card
from logic.card_controller import CardController

app = FastAPI()
st_object = CardController()
#app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    print('Request for index page received')
    return templates.TemplateResponse('CrearTarjeta.html', {"request": request})


@app.post('/consultar', response_class=HTMLResponse)
def consultar(request: Request, id: str = Form(...),tipo:str=Form(...),saldo:str=Form(...)):
    if id:
        return templates.TemplateResponse('ConsultarTarjeta.html', {"request": request, 'id': id,'tipo':tipo,'saldo':saldo})
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return RedirectResponse(request.url_for("index"), status_code=status.HTTP_302_FOUND)


@app.get("/")
def read_root():
    return {"200": "Welcome To Student Restful API"}


@app.get("/api/tarjeta")
async def root():
    return st_object.show()


@app.post("/api/add_tarjeta")
async def add(identification: int, tipoo: str, saldoo: str):
    card_temp = Card(idn=id , tipo=tipoo, saldo=saldoo)
    print(card_temp)
    return st_object.add(card_temp)


if __name__ == "__main__":
    uvicorn.run('app:app')
