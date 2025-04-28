from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})

def add_middlewares(app: FastAPI):
    app.middleware("http")(catch_exceptions_middleware)