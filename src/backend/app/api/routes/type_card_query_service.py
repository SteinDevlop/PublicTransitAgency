from fastapi import APIRouter, HTTPException, Security
from fastapi import status
from backend.app.models.type_card import TypeCardOut
from backend.app.logic.universal_controller_sql import UniversalController
from backend.app.core.auth import get_current_user

# Initialize the controller for type card operations
controller = UniversalController()

# Create the router with prefix and tags
app = APIRouter(prefix="/typecard", tags=["Type Card"])


@app.get("/typecards/")
def read_all(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Fetches all records of TypeCard.

    Args:
        current_user (dict): The current user, validated via security.
    
    Returns:
        List of TypeCard records.
    """
    return controller.read_all(TypeCardOut)


@app.get("/{id}")
def get_by_id(
    id: int, 
    current_user: dict = Security(get_current_user, scopes=["system", "administrador"])
):
    """
    Fetches a TypeCard record by its ID.

    Args:
        id (int): The ID of the TypeCard to retrieve.
        current_user (dict): The current user, validated via security.
    
    Raises:
        HTTPException: If the TypeCard is not found (404).
    
    Returns:
        TypeCard record details as a dictionary.
    """
    result = controller.get_by_id(TypeCardOut, id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="TypeCard not found"
        )
    return result.to_dict()
