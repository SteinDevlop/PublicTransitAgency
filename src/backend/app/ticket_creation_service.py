# maintainance_status_create.py
from fastapi import FastAPI, Form
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

@app.post("/maintainance_status/create")
async def create_maintainance_status(
    id: int = Form(...),
    unit: str = Form(...),
    type: str = Form(...),
    status: str = Form(...)
):
    ticket = Ticket(id=id, unit=unit, type=type, status=status)
    controller.add(ticket)
    return {"message": "Ticket registrado correctamente", "estado": ticket.__dict__}
