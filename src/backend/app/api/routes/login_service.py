import logging
from starlette.responses import HTMLResponse, RedirectResponse
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, Request, HTTPException, status, APIRouter, Form, Security
from fastapi.templating import Jinja2Templates
from backend.app.core.auth import encode_token, settings
from backend.app.logic.universal_controller_instance import universal_controller as controller
from backend.app.models.user import UserCreate, UserOut
from fastapi.responses import JSONResponse
from backend.app.core.auth import get_current_user

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = APIRouter(prefix="/login", tags=["login"])
templates = Jinja2Templates(directory="src/frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def login_form(request: Request):
    print("[LOGIN GET] Rendering login form")
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        logger.info("[POST /token] Attempting login for username: %s", form_data.username)

        # Validar que el username sea un número si la columna ID es de tipo int
        if not form_data.username.isdigit():
            logger.warning("[POST /token] Invalid username format: %s. Expected numeric ID.", form_data.username)
            raise HTTPException(status_code=400, detail="El ID debe ser un número.")

        # Convertir el username a entero antes de pasarlo al controlador
        user_id = int(form_data.username)
        user = controller.get_by_column(UserOut, "ID", user_id)

        if not user:
            logger.warning("[POST /token] User not found: %s", form_data.username)
            raise HTTPException(status_code=401, detail="Incorrect username or password")

        if user.Contrasena != form_data.password:
            logger.warning("[POST /token] Incorrect password for user: %s", form_data.username)
            raise HTTPException(status_code=401, detail="Incorrect username or password")

        scope = map_role_to_scope(user.IDRolUsuario)
        logger.info("[POST /token] User scope: %s", scope)

        # Generar el token con el campo 'sub' como el ID único del usuario
        payload = {
            "sub": str(user.ID),  # <-- Asegúrate de que sea string
            "scope": scope
        }

        token = encode_token(payload)
        logger.info("[POST /token] Token generated successfully for user: %s", form_data.username)

        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error("[POST /token] Error occurred: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/", response_class=HTMLResponse)
async def login_user(request: Request, username: str = Form(...), password: str = Form(...)):
    print(f"[LOGIN POST] Attempting login for ID: {username}")
    user = controller.get_by_column(UserOut, "ID", username)
    print(f"[LOGIN POST] Resultado de user: {user}")
    if not user or user.Contrasena != password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    scope = map_role_to_scope(user.IDRolUsuario)

    payload = {
        "sub": username,
        "scope": scope
    }

    token = encode_token(payload)
    response = RedirectResponse(url=request.url_for("get_scope_page", scope=scope), status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True, secure=True)
    return response

@app.get("/user/{scope}", name="get_scope_page", response_class=HTMLResponse)
async def get_scope_page(request: Request, scope: str):
    try:
        token_cookie = request.cookies.get("access_token", "").replace("Bearer ", "")
        user_data = {"username": "Unknown", "scope": scope}

        if token_cookie:
            try:
                payload = jwt.decode(token_cookie, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                user_data["username"] = payload.get("sub", "Unknown")
                user_data["scope"] = payload.get("scope", "Unknown")
            except JWTError as e:
                print(f"[SCOPE GET] Token decode error: {e}")

        user = controller.get_by_column(UserOut, "ID", user_data["username"])
        user_id = user.ID if user else "No ID found"

        return templates.TemplateResponse(f"{scope}.html", {
            "request": request,
            "user": user,
            "id": user_id,
            "total_vehiculos": controller.total_unidades(),
            "total_passanger": controller.total_pasajeros(),
            "total_operative": controller.total_operarios(),
            "total_supervisors": controller.total_supervisores(),
            "type_card": controller.last_card_used(user_id),
            "buses_mantenimiento": controller.total_unidades(),
            "registros_mantenimiento": controller.total_mantenimiento(),
            "proximo_mantenimiento": controller.proximos_mantenimientos(),
            "ultimo_uso_tarjeta": controller.last_card_used(user_id),
            "turno":controller.get_turno_usuario(user_id)
        })
    except Exception as e:
        print(f"[SCOPE GET] ERROR: {e}")
        return HTMLResponse(f"<h1>Template error: {e}</h1>", status_code=500)

@app.get("/dashboard")
async def general_dashboard(
    current_user: dict = Security(get_current_user, scopes=["system", "administrador", "supervisor", "operario", "pasajero", "mantenimiento"])
):
    logger.info("[DASHBOARD] Iniciando solicitud para el dashboard")

    user_id = current_user.get("sub")
    logger.info(f"[DASHBOARD] user_id (tipo: {type(user_id)}): {user_id}")
    try:
        user_id_int = int(user_id)
        user = controller.get_by_column(UserOut, "ID", user_id_int)
        if not user:
            logger.warning("[DASHBOARD] Usuario no encontrado en la base de datos para ID: %s", user_id)
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        logger.info("[DASHBOARD] Usuario encontrado en la base de datos: %s", user.Nombre)

        # Construir la respuesta del dashboard
        try:
            user_data = user.dict() if hasattr(user, 'dict') else user.__dict__
        except Exception as e:
            logger.error(f"[DASHBOARD] Error al serializar usuario: {e}")
            user_data = {}
        try:
            response_data = {
                "user": user_data,
                "id": user.ID,
                "total_vehiculos": controller.total_unidades(),
                "total_passanger": controller.total_pasajeros(),
                "total_operative": controller.total_operarios(),
                "total_supervisors": controller.total_supervisores(),
                "type_card": controller.last_card_used(user.ID),
                "buses_mantenimiento": controller.total_unidades(),
                "registros_mantenimiento": controller.total_mantenimiento(),
                "proximo_mantenimiento": controller.proximos_mantenimientos(),
                "ultimo_uso_tarjeta": controller.last_card_used(user.ID),
                #"turno": controller.get_turno_usuario(user.ID)
            }
        except Exception as e:
            logger.error(f"[DASHBOARD] Error al construir datos del dashboard: {e}")
            raise HTTPException(status_code=500, detail=f"Error interno al construir dashboard: {e}")

        logger.info("[DASHBOARD] Respuesta del dashboard generada correctamente")
        return JSONResponse(response_data)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(f"[DASHBOARD] Error inesperado: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno inesperado: {e}")
def map_role_to_scope(role_id: int) -> str:
    role_scope_map = {
        1: "pasajero",
        2: "operario",
        3: "supervisor",
        4: "administrador",
        5: "mantenimiento"
    }
    return role_scope_map.get(role_id, "guest")

