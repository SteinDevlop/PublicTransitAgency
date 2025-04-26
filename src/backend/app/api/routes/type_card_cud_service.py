from fastapi import APIRouter, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from backend.app.models.type_card import TypeCardOut, TypeCardCreate
from backend.app.logic.universal_controller_sql import UniversalController

# Inicializar el router y el controlador
app = APIRouter(prefix="/typecard", tags=["Type Card"])
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Ruta para crear un nuevo tipo de tarjeta
@app.get("/crear", response_class=HTMLResponse)
def crear_tipo_tarjeta(request: Request):
    return templates.TemplateResponse("CrearTipoTarjeta.html", {"request": request})

# Ruta para eliminar un tipo de tarjeta
@app.get("/eliminar", response_class=HTMLResponse)
def eliminar_tipo_tarjeta(request: Request):
    return templates.TemplateResponse("EliminarTipoTarjeta.html", {"request": request})

# Ruta para actualizar un tipo de tarjeta
@app.get("/actualizar", response_class=HTMLResponse)
def actualizar_tipo_tarjeta(request: Request):
    return templates.TemplateResponse("ActualizarTipoTarjeta.html", {"request": request})

# Ruta para agregar un tipo de tarjeta
@app.post("/create")
async def add_typecard(
    id: int = Form(...),
    type: str = Form(...)
):
    try:
        # Crear una nueva tarjeta con los datos proporcionados
        new_typecard = TypeCardCreate(id=id, type=type)
        
        # Llamamos al controlador para agregar la tarjeta
        result = controller.add(new_typecard)
        
        # Retornar la respuesta de éxito
        return {
            "operation": "create",
            "success": True,
            "data": TypeCardOut(id=new_typecard.id, type=new_typecard.type).dict(),
            "message": "Tipo de tarjeta creado correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Error interno del servidor: {str(e)}")

# Ruta para actualizar un tipo de tarjeta
@app.post("/update")
async def update_typecard(
    id: int = Form(...),
    type: str = Form(...)
):
    try:
        # Buscar el tipo de tarjeta existente para actualizar
        existing = controller.get_by_id(TypeCardOut, id)
        if not existing:
            raise HTTPException(404, detail="Tipo de tarjeta no encontrado")
        
        # Crear una nueva instancia con los datos actualizados
        updated_typecard = TypeCardCreate(id=id, type=type)
        
        # Llamamos al controlador para actualizar la tarjeta
        result = controller.update(updated_typecard)
        
        # Retornar la respuesta de éxito
        return {
            "operation": "update",
            "success": True,
            "data": TypeCardOut(id=updated_typecard.id, type=updated_typecard.type).dict(),
            "message": f"Tipo de tarjeta {id} actualizado correctamente"
        }
    except ValueError as e:
        raise HTTPException(400, detail=str(e))

# Ruta para eliminar un tipo de tarjeta
@app.post("/delete")
async def delete_typecard(id: int = Form(...)):
    try:
        # Buscar el tipo de tarjeta para eliminar
        existing = controller.get_by_id(TypeCardOut, id)
        if not existing:
            raise HTTPException(404, detail="Tipo de tarjeta no encontrado")
        
        # Llamamos al controlador para eliminar la tarjeta
        controller.delete(existing)
        
        # Retornar la respuesta de éxito
        return {
            "operation": "delete",
            "success": True,
            "message": f"Tipo de tarjeta {id} eliminado correctamente"
        }
    except Exception as e:
        raise HTTPException(500, detail=str(e))

