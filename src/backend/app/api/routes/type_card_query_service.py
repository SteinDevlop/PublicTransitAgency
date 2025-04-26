from fastapi import FastAPI, HTTPException,APIRouter, Form, Request, status,Query
from backend.app.models.type_card import TypeCardOut, TypeCardCreate
from backend.app.logic.universal_controller_sql import UniversalController

controller = UniversalController()
app = APIRouter(prefix="/typecard", tags=["Type Card"])

@app.get("/typecards/")
def read_all():
    return controller.read_all(TypeCardOut)
@app.get("/{id}")
def get_by_id(id: int):
    """
    Retorna un registro de TypeCard por su ID.
    """
    result = controller.get_by_id(TypeCardOut, id)
    if not result:
        raise HTTPException(status_code=404, detail="No encontrado")
    return result.to_dict()
