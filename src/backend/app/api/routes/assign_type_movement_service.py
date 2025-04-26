from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.app.models.type_movement import TypeMovementCreate, TypeMovementOut
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

@app.post('/typemovement')
def crear_registro(tipo_mov: TypeMovementCreate):
    return controller.add(tipo_mov)

@app.get('/typemovement')
def obtener_todos_los_detalle_tipo_movimiento():
    # Enviar clase para que UniversalController obtenga el nombre
    return controller.read_all(TypeMovementCreate)

@app.get('/typemovement/{id}')
def obtener_tipo_movimiento_con_id(id: int):
    return controller.get_by_id(TypeMovementOut, id)

@app.put('/typemovement/{id}')
def editar_tipo_movimiento(id: int, atributo: str, valor: str):
    tipo_mov = controller.get_by_id(TypeMovementOut, id)
    if not tipo_mov:
        return {"error": "TypeMovement not found"}

    setattr(tipo_mov, atributo, valor)
    return controller.update(tipo_mov)

@app.delete('/typemovement/{id}')
def eliminar_tipo_movimiento(id: int):
    tipo_mov = controller.get_by_id(TypeMovementOut, id)
    if not tipo_mov:
        return {"error": "TypeMovement not found"}

    controller.delete(tipo_mov)
    return {"status": "Deleted succesfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
