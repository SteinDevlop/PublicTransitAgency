from fastapi import FastAPI, Form, Request, status, Query
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from logic.payments import Payments
from logic.payments_controller import PaymentsController

app = FastAPI()
st_object = PaymentsController()

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
'''
Considera que debe haber un limite maximo y minimo por transaccion (ya sea que no se puede recargar mas de cierto valor)
'''
def generar_registro(id_tarjeta,tipo_transporte,tipo_pago,valor,fecha):
    pass #Enviar al servicio de movement
@app.post('/payment/tarjeta/{id}/recarga')
def recargar(request: Request):
    #Puede tener pagina web para aplicar la recarga
    #Genera recibo de la recarga
    #Debe recargar el saldo de la tarjeta. Debe llamar generar registro
    pass
@app.post('/payment/tarjeta/{id}/uso')
def uso(request: Request):
    pass
    #debe llamarse cuando se usa la tarjeta en un transporte especifico
    #Puede mostrar pagina web con la cantidad de saldo despues del pago
    #Debe descontar una cantidad del saldo de la tarjeta. Debe llamar generar registro
if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)