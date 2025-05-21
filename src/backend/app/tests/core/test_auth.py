import pytest
from fastapi import Request, HTTPException, status
from fastapi.security import SecurityScopes
from backend.app.core import auth
from types import SimpleNamespace
from jose import jwt

class DummySettings:
    SECRET_KEY = "testsecret"
    ALGORITHM = "HS256"

def make_token(payload):
    return jwt.encode(payload, DummySettings.SECRET_KEY, algorithm=DummySettings.ALGORITHM)

@pytest.fixture(autouse=True)
def patch_settings(monkeypatch):
    monkeypatch.setattr(auth, "settings", DummySettings)

@pytest.fixture
def dummy_request():
    class DummyRequest:
        def __init__(self, cookies=None):
            self.cookies = cookies or {}
    return DummyRequest

def test_encode_token():
    payload = {"sub": "123", "scope": "admin"}
    token = auth.encode_token(payload)
    decoded = jwt.decode(token, DummySettings.SECRET_KEY, algorithms=[DummySettings.ALGORITHM])
    assert decoded["sub"] == "123"
    assert decoded["scope"] == "admin"

def test_get_current_user_valid_token(dummy_request):
    token = make_token({"sub": "1", "scope": "admin"})
    scopes = SecurityScopes([])
    req = dummy_request()
    user = auth.get_current_user(scopes, req, token)
    assert user["sub"] == "1"
    assert user["scope"] == "admin"

def test_get_current_user_token_from_cookie(dummy_request):
    token = make_token({"sub": "2", "scope": "admin"})
    scopes = SecurityScopes([])
    req = dummy_request({"access_token": f"Bearer {token}"})
    user = auth.get_current_user(scopes, req, "")
    assert user["sub"] == "2"
    assert user["scope"] == "admin"

def test_get_current_user_no_token(dummy_request):
    scopes = SecurityScopes([])
    req = dummy_request()
    with pytest.raises(HTTPException) as exc:
        auth.get_current_user(scopes, req, "")
    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user_invalid_token(dummy_request):
    scopes = SecurityScopes([])
    req = dummy_request()
    with pytest.raises(HTTPException) as exc:
        auth.get_current_user(scopes, req, "badtoken")
    assert exc.value.status_code == 401

def test_get_current_user_missing_fields(dummy_request):
    token = make_token({"foo": "bar"})
    scopes = SecurityScopes([])
    req = dummy_request()
    with pytest.raises(HTTPException) as exc:
        auth.get_current_user(scopes, req, token)
    assert exc.value.status_code == 401

def test_verify_role_allows():
    allowed_roles = ["admin", "system"]
    _verify = auth.verify_role(allowed_roles)
    # Llama directamente a la función interna pasando un dict simulado
    assert _verify({"scopes": ["admin", "system"]}) == {"scopes": ["admin", "system"]}

def test_verify_role_denies():
    allowed_roles = ["admin", "system"]
    _verify = auth.verify_role(allowed_roles)
    with pytest.raises(HTTPException) as exc:
        _verify({"scopes": ["pasajero"]})
    assert exc.value.status_code == status.HTTP_403_FORBIDDEN
