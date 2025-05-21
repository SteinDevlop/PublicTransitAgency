import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.app.core.middlewares import add_middlewares

@pytest.fixture
def app_with_middleware():
    app = FastAPI()
    add_middlewares(app)

    @app.get("/ok")
    async def ok():
        return {"msg": "ok"}

    @app.get("/fail")
    async def fail():
        raise Exception("fail")

    return app

def test_ok_response(app_with_middleware):
    client = TestClient(app_with_middleware)
    response = client.get("/ok")
    assert response.status_code == 200
    assert response.json() == {"msg": "ok"}

def test_exception_caught(app_with_middleware):
    client = TestClient(app_with_middleware)
    response = client.get("/fail")
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}
