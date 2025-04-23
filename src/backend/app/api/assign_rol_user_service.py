from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from logic.rol_user import RolUserCreate, RolUserOut
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

@app.post('/roluser')
def crear_registro(tipo_mov: RolUserCreate):
    return controller.add(tipo_mov)

@app.get('/roluser')
def obtener_todos_los_detalle_rol_usuario():
    # Enviar clase para que UniversalController obtenga el nombre
    return controller.read_all(RolUserCreate)

@app.get('/roluser/{id}')
def obtener_rol_usuario_con_id(id: int):
    return controller.get_by_id(RolUserCreate, id)

@app.put('/roluser/{id}')
def editar_rol_usuario(id: int, atributo: str, valor: str):
    tipo_mov = controller.get_by_id(RolUserOut, id)
    if not tipo_mov:
        return {"error": "RolUser not found"}

    setattr(tipo_mov, atributo, valor)
    return controller.update(tipo_mov)

@app.delete('/roluser/{id}')
def eliminar_rol_usuario(id: int):
    tipo_mov = controller.get_by_id(RolUserOut, id)
    if not tipo_mov:
        return {"error": "RolUser not found"}

    controller.delete(tipo_mov)
    return {"status": "Deleted succesfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
