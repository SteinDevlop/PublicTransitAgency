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
        # Log seguro de los datos de entrada ANTES de usarlos
        for label, value in [("ubicacion_entrada", ubicacion_entrada), ("ubicacion_final", ubicacion_final)]:
            if value.isalnum():
                logger.log(logging.CRITICAL, "%s: %s", label, value)
            else:
                logger.log(
                    logging.CRITICAL,
                    "%s (Invalid Input, base64): %s",
                    label,
                    base64.b64encode(value.encode('UTF-8')).decode()
                )

        resultado = controller.obtener_ruta_con_interconexion(ubicacion_entrada, ubicacion_final)
        
        if not resultado:
            logger.log(logging.CRITICAL, "Resultado vacío o inválido")
        return resultado
    except Exception as e:
        logger.error("Error al obtener las rutas con interconexión: %s", str(e))