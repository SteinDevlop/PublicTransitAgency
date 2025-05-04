#type_movement_query_service.py
# # This module provides a query service for TypeMovement using FastAPI.
# # It includes routes for retrieving all TypeMovement records and getting a specific record by ID.

from fastapi import FastAPI, HTTPException, APIRouter, Form, Request, status, Query
from backend.app.models.type_movement import TypeMovementCreate, TypeMovementOut
from backend.app.logic.universal_controller_sql import UniversalController

controller = UniversalController()
app = APIRouter(prefix="/typemovement", tags=["Type Movement"])

@app.get("/typemovements/")
def read_all():
    """
    Returns all records of TypeMovement.
    """
    return controller.read_all(TypeMovementOut)

@app.get("/{id}")
def get_by_id(id: int):
    """
    Returns a TypeMovement record by its ID.
    If not found, raises a 404 error.
    """
    result = controller.get_by_id(TypeMovementOut, id)
    if not result:
        raise HTTPException(status_code=404, detail="Not found")
    return result.to_dict()

