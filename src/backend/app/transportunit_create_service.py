# transport_unit_create.py
from fastapi import FastAPI, Form, Request
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

@app.post("/transport_unit/create")
async def create_transport_unit(
    id: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),  # se espera un string, por ahora simulamos
    ubication: str = Form(...),
    capacity: int = Form(...)
):
    transport_unit = Transport(id=id, type=type, status=status, ubication=ubication, capacity=capacity)
    controller.add(transport_unit)
    return {"message": "Unidad de transporte creada correctamente", "unidad": transport_unit.__dict__}
