from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.app.models.price import PriceCreate, PriceOut
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

@app.post('/price')
def crear_registro(price: PriceCreate):
    return controller.add(price)

@app.get('/price')
def obtener_todos_los_detalle_precio():
    return controller.read_all(PriceCreate)

@app.get('/price/{id}')
def obtener_precio_con_id(id: int):
    return controller.get_by_id(PriceOut, id)

@app.put('/price/{id}')
def editar_precio(id: int, atributo: str, valor: str):
    price_temp = controller.get_by_id(PriceOut, id)
    if not price_temp:
        return {"error": "Price not found"}

    setattr(price_temp, atributo, valor)
    return controller.update(price_temp)

@app.delete('/price/{id}')
def eliminar_precio(id: int):
    price_temp = controller.get_by_id(PriceOut, id)
    if not price_temp:
        return {"error": "Price not found"}

    controller.delete(price_temp)
    return {"status": "Deleted successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
