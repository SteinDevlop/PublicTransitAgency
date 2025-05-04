#rol_user_query_service.py


from fastapi import FastAPI, HTTPException, APIRouter, Form, Request, status, Query
from backend.app.models.rol_user import RolUserCreate, RolUserOut
from backend.app.logic.universal_controller_sql import UniversalController

controller = UniversalController()
app = APIRouter(prefix="/roluser", tags=["Rol User"])

@app.get("/rolusers/")
def read_all():
    """
    Returns all records of RolUser.
    """
    return controller.read_all(RolUserOut)

@app.get("/{id}")
def get_by_id(id: int):
    """
    Returns a RolUser record by its ID.
    If not found, raises a 404 error.
    """
    result = controller.get_by_id(RolUserOut, id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result.to_dict()

