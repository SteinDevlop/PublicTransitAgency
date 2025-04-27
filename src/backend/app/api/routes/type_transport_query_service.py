from fastapi import FastAPI, HTTPException, APIRouter, Form, Request, status, Query
from backend.app.models.type_transport import TypeTransportCreate, TypeTransportOut
from backend.app.logic.universal_controller_sql import UniversalController

controller = UniversalController()
app = APIRouter(prefix="/typetransport", tags=["Type Transport"])

@app.get("/typetransports/")
def read_all():
    """
    Returns all records of TypeTransport.
    """
    return controller.read_all(TypeTransportOut)

@app.get("/{id}")
def get_by_id(id: int):
    """
    Returns a TypeTransport record by its ID.
    If not found, raises a 404 error.
    """
    result = controller.get_by_id(TypeTransportOut, id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result.to_dict()

