from fastapi import FastAPI, Form, Request, status, Query
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from logic.movement import Movement
from logic.movement_controller import MovementController

app = FastAPI()
st_object = MovementController()

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
@app.post('/movement/tarjetas/{id}/movimientos')
def crear_registro(request: Request):
    pass
@app.get('/movement/tarjetas/{id}/movimientos/{movimiento_id}')
def obtener_detalle_movimiento(id: int, movimiento_id: int):
    pass
@app.get('/movement/tarjetas/{id}/movimientos')
def obtener_todos_los_movimientos(id: int):
    pass
@app.put('/movement/tarjetas/{id}/movimientos/{movimiento_id}')
def editar_movimiento(id: int, movimiento_id: int, request: Request):
    pass
@app.delete('/movement/tarjetas/{id}/movimientos/{movimiento_id}')
def eliminar_movimiento(id: int, movimiento_id: int):
    pass
if __name__ == "__main__":
    uvicorn.run("app:app", reload=True)