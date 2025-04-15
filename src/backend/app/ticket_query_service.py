# maintainance_status_list_all.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logic.ticket import Ticket
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

@app.get("/ticket/all")
def get_all_ticket():
    estados = controller.read_all(Ticket(0, "", "", ""))
    return {"estados_mantenimiento": estados}

@app.get("/maintainance_status/{id}")
def get_tickets_by_id(id: int):
    estado = controller.get_by_id(Ticket, id)
    if estado:
        return {"Ticket": estado.__dict__}
    return {"error": "Ticket no encontrado"}