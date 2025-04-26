from fastapi import FastAPI, Form, HTTPException,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from src.backend.app.models.card import CardCreate, CardOut  # Asegúrate de que tus modelos estén en este archivo
from  src.backend.app.logic.card_controller import CardController 
import uvicorn

app = APIRouter(prefix="/card", tags=["card"])
controller = CardController()  # Asegúrate de tener el controlador correspondiente

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],  
    allow_headers=["*"],
)

@app.post("/card/create")
async def create_card(
    id: int = Form(...),
    tipo: str = Form(...),
    saldo: float = Form(...)
):
    try:
        # Crear una instancia del modelo CardCreate para validar los datos de entrada
        new_card = CardCreate(
            id=id,
            tipo=tipo,
            balance=saldo
        )
        # Usamos el controlador para agregar la tarjeta (convertimos el modelo a dict)
        result = controller.add(new_card.to_dict())
        
        # Devolvemos la respuesta utilizando CardOut para devolver los datos de la tarjeta
        return {
            "operation": "create",
            "success": True,
            "data": CardOut(id=new_card.id, tipo=new_card.tipo, balance=new_card.balance).dict(),
            "message": "Tarjeta creada correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail="Error interno del servidor")

@app.post("/card/update")
async def update_card(
    id: int = Form(...),
    tipo: str = Form(...),
    saldo: float = Form(...)
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
            balance=saldo
        )
        # Usamos el controlador para actualizar la tarjeta (convertimos el modelo a dict)
        result = controller.update(updated_card.to_dict())
        
        # Devolvemos la respuesta con la tarjeta actualizada utilizando CardOut
        return {
            "operation": "update",
            "success": True,
            "data": CardOut(id=updated_card.id, tipo=updated_card.tipo, balance=updated_card.balance).dict(),
            "message": f"Tarjeta {id} actualizada correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

@app.post("/card/delete")
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
