from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logic.maintainance_status import MaintainanceStatus
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

@app.get("/maintainance_status/all")
def get_all_maintainance_status():
    estados = controller.read_all(MaintainanceStatus(0, "", "", ""))
    return {"estados_mantenimiento": estados}

@app.get("/maintainance_status/{id}")
def get_maintainance_status_by_id(id: int):
    estado = controller.get_by_id(MaintainanceStatus, id)
    if estado:
        return {"estado_mantenimiento": estado.__dict__}
    return {"error": "Estado de mantenimiento no encontrado"}