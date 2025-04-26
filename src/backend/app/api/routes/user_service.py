from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from logic.user import UserCreate, UserOut
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

@app.post('/user')
def crear_registro(tipo_mov: UserCreate):
    return controller.add(tipo_mov)

@app.get('/user')
def obtener_todos_los_detalle_usuario():
    # Enviar clase para que UniversalController obtenga el nombre
    return controller.read_all(UserCreate)

@app.get('/user/{id}')
def obtener_tipo_usuario_con_id(id: int):
    return controller.get_by_id(UserCreate, id)

@app.put('/user/{id}')
def editar_usuario(id: int, atributo: str, valor: str):
    tipo_mov = controller.get_by_id(UserOut, id)
    if not tipo_mov:
        return {"error": "User not found"}

    setattr(tipo_mov, atributo, valor)
    return controller.update(tipo_mov)

@app.delete('/user/{id}')
def eliminar_usuario(id: int):
    tipo_mov = controller.get_by_id(UserOut, id)
    if not tipo_mov:
        return {"error": "User not found"}

    controller.delete(tipo_mov)
    return {"status": "Deleted succesfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
