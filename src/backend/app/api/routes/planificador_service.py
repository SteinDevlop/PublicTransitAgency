import logging
from fastapi import (
    Form, HTTPException, APIRouter, Request, Security
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import base64
from backend.app.models.card import CardCreate, CardOut
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.core.auth import get_current_user

# Configuración de logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = APIRouter(prefix="/planificador", tags=["Planificador"])

@app.post("/ubicaciones")
async def get_route_plan(request: Request, ubicacion_entrada: str = Form(...), ubicacion_final: str = Form(...)):
    try:
        # Intentamos obtener el resultado de la interconexión
        resultado = controller.obtener_ruta_con_interconexion(ubicacion_entrada, ubicacion_final)
        
        # Verificamos si el resultado es vacío o None, y gestionamos el error
        if resultado:
            logger.log(logging.CRITICAL, "%s", ubicacion_entrada,ubicacion_final)
        else:
            logger.log(logging.CRITICAL, "Invalid Input: %s", base64.b64encode(resultado.encode('UTF-8')))
        # Si todo está bien, retornamos el resultado a la plantilla
        return resultado
    except Exception as e:
        # Logueamos el error si algo falla
        logger.error(f"Error al obtener las rutas con interconexión: {str(e)}")
        # Retornamos un mensaje de error al usuario