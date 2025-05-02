from fastapi import Depends, HTTPException, status, Request, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import jwt, JWTError
from backend.app.core.config import settings
from typing import Dict, List

# OAuth2 con scopes definidos
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login",  # debe coincidir con tu endpoint real de generación de token
    scopes={
        "system": "Acceso completo al sistema",
        "administrador": "Permiso para gestionar usuarios",
        "pasajero": "Permiso de pasajero",
        "supervisor": "Permiso de supervisor",
        "mantenimiento": "Permiso de mantenimiento",
        "operador": "Permiso de operador",
    }
)

# Función para codificar el token
def encode_token(payload: dict) -> str:
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# Función para obtener al usuario actual autenticado
def get_current_user(
    security_scopes: SecurityScopes,
    request: Request,
    token: str = Depends(oauth2_scheme)
) -> Dict[str, str]:
    token_cookie = request.cookies.get("access_token")
    if token_cookie:
        token = token_cookie.replace("Bearer ", "")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authenticated",
        )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        scope_string = payload.get("scope", "")
        token_scopes = scope_string.split()

        return {
            "user_id": user_id,
            "scopes": token_scopes
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
# Verificación adicional por roles (scopes)
def verify_role(allowed_roles: List[str]):
    def _verify(current_user: dict = Depends(get_current_user)):
        if not any(scope in allowed_roles for scope in current_user["scopes"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a esta ruta",
            )
        return current_user
    return _verify
