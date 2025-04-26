from fastapi import FastAPI, Form, HTTPException,APIRouter,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from backend.app.models.card import CardCreate, CardOut  # Asegúrate de que tus modelos estén en este archivo
from  backend.app.logic.universal_controller_sql import UniversalController 
import uvicorn

app = APIRouter(prefix="/card", tags=["card"])
controller = UniversalController()  # Asegúrate de tener el controlador correspondiente
templates = Jinja2Templates(directory="src/backend/app/templates")
@app.get("/crear", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("CrearTarjeta.html", {"request": request})
@app.get("/actualizar", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("ActualizarTarjeta.html", {"request": request})
@app.get("/eliminar", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("EliminarTarjeta.html", {"request": request})
@app.post("/create")
async def create_card(
    id: int = Form(...),
    tipo: str = Form(...),
):
    try:
        new_card = CardCreate(
            id=id,
            tipo=tipo,
            balance=0
        )
        # AQUÍ: NO LLAMES to_dict()
        result = controller.add(new_card)
        
        return {
            "operation": "create",
            "success": True,
            "data": CardOut(id=new_card.id, tipo=new_card.tipo, balance=new_card.balance).dict(),
            "message": "Tarjeta creada correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Error interno del servidor: {str(e)}")

@app.post("/update")
async def update_card(
    id: int = Form(...),
    tipo: str = Form(...),
):
    try:
        # Buscar la tarjeta existente para actualización
        existing = controller.get_by_id(CardOut, id)  # Aquí usamos CardOut para buscar la tarjeta
        if not existing:
            raise HTTPException(404, detail="Tarjeta no encontrada")
        
        # Crear una instancia del modelo CardCreate para validar los datos de actualización
        updated_card = CardCreate(
            id=id,
            tipo=tipo,
            saldo=existing.balance
        )
        # Usamos el controlador para actualizar la tarjeta (convertimos el modelo a dict)
        result = controller.update(updated_card)
        
        # Devolvemos la respuesta con la tarjeta actualizada utilizando CardOut
        return {
            "operation": "update",
            "success": True,
            "data": CardOut(id=updated_card.id, tipo=updated_card.tipo, balance=updated_card.balance).dict(),
            "message": f"Tarjeta {id} actualizada correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/delete")
async def delete_card(id: int = Form(...)):
    try:
        # Buscar la tarjeta para eliminar
        existing = controller.get_by_id(CardOut, id)  # Usamos CardOut para buscar la tarjeta
        if not existing:
            raise HTTPException(404, detail="Tarjeta no encontrada")
        
        # Usamos el controlador para eliminar la tarjeta
        controller.delete(existing)
        
        return {
            "operation": "delete",
            "success": True,
            "message": f"Tarjeta {id} eliminada correctamente"
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "app:app",  # Asegúrate de que tu archivo se llame app.py
        host="0.0.0.0",
        port=8001,  # Cambia el puerto si es necesario
        reload=True
    )
