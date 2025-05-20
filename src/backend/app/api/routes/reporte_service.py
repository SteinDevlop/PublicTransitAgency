import logging
import json
from fastapi import Request, APIRouter,Security
from fastapi.responses import JSONResponse
from backend.app.core.auth import get_current_user

from backend.app.logic.universal_controller_instance import universal_controller as controller

# Configuración del logger
logger = logging.getLogger("reporte_logger")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Crear el enrutador para los endpoints de reporte
app = APIRouter(prefix="/reporte", tags=["Reporte"])

# Inicializar el controlador universal

@app.get("/supervisor")
async def get_supervisor_report(request: Request,current_user: dict = Security(get_current_user,scopes=["system", "administrador","supervisor"])):
    try:
        # Obtener datos desde el controlador
        report_data = {
            "total_movimientos": controller.total_movimientos(),
            "total_usuarios": controller.total_usuarios(),
            "promedio_horas_trabajadas": controller.promedio_horas_trabajadas(),
        }
        logger.info("Reporte de supervisor generado exitosamente.")
        return report_data
    except Exception as e:
        # Log de error con detalles
        logger.error(f"Error al generar el reporte de supervisor: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Ocurrió un error al generar el reporte de supervisor."}
        )

@app.get("/alert-tec")
async def get_technical_alert_report(request: Request,current_user: dict = Security(get_current_user,scopes=["system", "administrador","mantenimiento"])):
    try:
        # Obtener datos desde el controlador
        atrasados = controller.alerta_mantenimiento_atrasados()
        proximos = controller.alerta_mantenimiento_proximos()

        # Convertir los datos a un formato serializable
        def serialize(obj):
            if hasattr(obj, "to_dict"):
                return obj.to_dict()
            elif hasattr(obj, "__dict__"):
                return vars(obj)
            else:
                return str(obj)  # Convertir a string como último recurso

        report_data = {
            "mantenimientos_atrasados": [serialize(obj) for obj in atrasados],
            "mantenimientos_proximos": [serialize(obj) for obj in proximos],
        }

        logger.info("Reporte técnico generado exitosamente.")
        logger.info(f"Datos del reporte técnico: {report_data}")

        # Validar si los datos son serializables a JSON
        try:
            json.dumps(report_data)  # Intentar serializar los datos
        except TypeError as e:
            logger.error(f"Datos no serializables a JSON: {e}")
            return JSONResponse(
                status_code=500,
                content={"detail": "Los datos del reporte no son válidos para JSON."}
            )

        # Devolver los datos como JSON
        return report_data
    except Exception as e:
        # Log de error con detalles
        logger.error(f"Error al generar el reporte técnico: {e}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Ocurrió un error al generar el reporte técnico."}
        )