from fastapi import FastAPI, HTTPException
from logic.type_card import TypeCard
from logic.universal_controller_sql import UniversalController

app = FastAPI()
controller = UniversalController()

@app.get("/typecard/")
def read_all():
    """
    Retorna todos los registros de TypeCard.
    """
    dummy = TypeCard(None, "")  # se necesita para que `read_all` sepa de qué tabla leer
    return controller.read_all(dummy)

@app.get("/typecard/{id}")
def get_by_id(id: int):
    """
    Retorna un registro de TypeCard por su ID.
    """
    result = controller.get_by_id(TypeCard, id)
    if not result:
        raise HTTPException(status_code=404, detail="No encontrado")
    return result.to_dict()
