from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from backend.app.models.routes import RouteCreate, RouteOut
from backend.app.logic.universal_controller_sql import UniversalController
import uvicorn

app = FastAPI()
controller = UniversalController()
templates = Jinja2Templates(directory="src/backend/app/templates")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Formulario para crear una nueva ruta
@app.get("/routes/crear", response_class=HTMLResponse, tags=["cud_routes"])
def show_create_form(request: Request):
    return templates.TemplateResponse("CrearRuta.html", {"request": request})

# Formulario para actualizar una ruta existente
@app.get("/routes/actualizar", response_class=HTMLResponse, tags=["cud_routes"])
def show_update_form(request: Request):
    return templates.TemplateResponse("ActualizarRuta.html", {"request": request})

# Formulario para eliminar una ruta existente
@app.get("/routes/eliminar", response_class=HTMLResponse, tags=["cud_routes"])
def show_delete_form(request: Request):
    return templates.TemplateResponse("EliminarRuta.html", {"request": request})

# Crear una nueva ruta
@app.post("/routes/crear", response_model=RouteOut, tags=["cud_routes"])
async def create_route(
    request: Request,
    route_id: str = Form(...),
    route_data: str = Form(...),  # Recibimos la ruta como string JSON
):
    try:
        import json
        route_dict = json.loads(route_data)
        new_route = RouteCreate(route_id=route_id, route=route_dict)
        result = controller.add(new_route)
        return RouteOut(route_id=result.route_id, route=result.route)
    except json.JSONDecodeError:
        raise HTTPException(400, detail="Formato JSON inválido para la ruta")
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Error interno del servidor: {str(e)}")

# Actualizar una ruta existente
@app.post("/routes/actualizar", response_model=RouteOut, tags=["cud_routes"])
async def update_route(
    request: Request,
    route_id: str = Form(...),
    route_data: str = Form(...),  # Recibimos la ruta como string JSON
):
    try:
        existing_route = controller.get_by_id(RouteOut, route_id)
        if not existing_route:
            raise HTTPException(404, detail="Ruta no encontrada")

        import json
        route_dict = json.loads(route_data)
        updated_route = RouteCreate(route_id=route_id, route=route_dict) # Usamos RouteCreate para la validación
        result = controller.update(updated_route)
        return RouteOut(route_id=result.route_id, route=result.route)
    except json.JSONDecodeError:
        raise HTTPException(400, detail="Formato JSON inválido para la ruta")
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"Error interno del servidor: {str(e)}")

# Eliminar una ruta existente
@app.post("/routes/eliminar", tags=["cud_routes"])
async def delete_route(request: Request, route_id: str = Form(...)):
    try:
        existing_route = controller.get_by_id(RouteOut, route_id)
        if not existing_route:
            raise HTTPException(404, detail="Ruta no encontrada")
        controller.delete(existing_route)
        return {"message": f"Ruta con ID {route_id} eliminada correctamente"}
    except Exception as e:
        raise HTTPException(500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app_cud_routes:app", host="0.0.0.0", port=8004, reload=True)