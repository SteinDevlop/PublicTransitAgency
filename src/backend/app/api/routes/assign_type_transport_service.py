from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.app.models.type_transport import TypeTransportCreate, TypeTransportOut
from logic.universal_controller_json import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/typetransportunit')
def crear_registro(price: TypeTransportCreate):
    return controller.add(price)

@app.get('/typetransportunit')
def obtener_todos_los_detalle_tipo_transporte():
    return controller.read_all(TypeTransportCreate)

@app.get('/typetransportunit/{id}')
def obtener_tipo_movimiento_con_id(id: int):
    return controller.get_by_id(TypeTransportOut, id)

@app.put('/typetransportunit/{id}')
def editar_tipo_transporte(id: int, atributo: str, valor: str):
    price_temp = controller.get_by_id(TypeTransportOut, id)
    if not price_temp:
        return {"error": "typetransportunit not found"}

    setattr(price_temp, atributo, valor)
    return controller.update(price_temp)

@app.delete('/typetransportunit/{id}')
def eliminar_tipo_transporte(id: int):
    price_temp = controller.get_by_id(TypeTransportOut, id)
    if not price_temp:
        return {"error": "typetransportunit not found"}

    controller.delete(price_temp)
    return {"status": "Deleted successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
