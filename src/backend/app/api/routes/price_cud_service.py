from fastapi import FastAPI, Form, HTTPException, APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.price import PriceCreate, PriceOut
from backend.app.logic.universal_controller_sql import UniversalController

app = FastAPI()
router = APIRouter(prefix="/price", tags=["price"])
templates = Jinja2Templates(directory="src/backend/app/templates")

def get_controller():
    return UniversalController()

@router.get("/crear", response_class=HTMLResponse)
def create_form(request: Request):
    return templates.TemplateResponse("CrearPrecio.html", {"request": request})

@router.get("/actualizar", response_class=HTMLResponse)
def update_form(request: Request):
    return templates.TemplateResponse("ActualizarPrecio.html", {"request": request})

@router.get("/eliminar", response_class=HTMLResponse)
def delete_form(request: Request):
    return templates.TemplateResponse("EliminarPrecio.html", {"request": request})

@router.post("/create")
async def create_price(id: int = Form(...), unidadtransportype: str = Form(...), amount: float = Form(...), controller: UniversalController = Depends(get_controller)):
    try:
        new_price = PriceCreate(id=id, unidadtransportype=unidadtransportype, amount=amount)
        controller.add(new_price)
        return {
            "operation": "create",
            "success": True,
            "data": PriceOut(**new_price.model_dump()).model_dump(),
            "message": "Price created successfully"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@router.post("/update")
async def update_price(id: int = Form(...), unidadtransportype: str = Form(...), amount: float = Form(...), controller: UniversalController = Depends(get_controller)):
    try:
        existing = controller.get_by_id(PriceOut, id)
        if existing is None:
            raise HTTPException(404, detail="Price not found")
        updated_price = PriceCreate(id=id, unidadtransportype=unidadtransportype, amount=amount)
        controller.update(updated_price)
        return {
            "operation": "update",
            "success": True,
            "data": PriceOut(**updated_price.model_dump()).model_dump(),
            "message": f"Price {id} updated successfully"
        }
    except HTTPException as e:
        raise e  # <-- Permitir que se propague tal como está
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")

@router.post("/delete")
async def delete_price(id: int = Form(...), controller: UniversalController = Depends(get_controller)):
    try:
        existing = controller.get_by_id(PriceOut, id)
        if existing is None:
            raise HTTPException(404, detail="Price not found")
        controller.delete(existing)
        return {
            "operation": "delete",
            "success": True,
            "message": f"Price {id} deleted successfully"
        }
    except HTTPException as e:
        raise e  # <-- Permitir que se propague tal como está
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Internal server error: {str(e)}")
app.include_router(router)
