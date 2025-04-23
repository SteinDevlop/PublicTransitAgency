from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logic.unit_transport import Transport
from logic.universal_controller_json import UniversalController

app = FastAPI()
controller = UniversalController()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/transport_unit/all")
def get_all_transport_units():
    unidades = controller.read_all(Transport("", "", "", "", 0))
    return {"unidades": unidades}

@app.get("/transport_unit/{id}")
def get_transport_unit_by_id(id: str):
    unidad = controller.get_by_id(Transport, id)
    if unidad:
        return {"unidad": unidad.__dict__}
    return {"error": "Unidad no encontrada"}
