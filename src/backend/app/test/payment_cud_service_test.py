from fastapi.testclient import TestClient
from src.backend.app.api.routes.payment_cud_service import app
from src.backend.app.models.card import Card

client = TestClient(app)

def test_get_schema_payment():
    response = client.get("/schema/payment")
    assert response.status_code == 200
    assert "fields" in response.json()
    assert any(f["name"] == "id" for f in response.json()["fields"])
    assert any(f["name"] == "valor" for f in response.json()["fields"])

def test_recharge_invalid_value_low(monkeypatch):
    monkeypatch.setattr("src.backend.app.api.routes.payment_cud_service.controller.get_by_id", lambda cls, id: Card(id=id, balance=1000))
    
    response = client.post("/payment/tarjeta/test-id/recarga", params={"valor": 500, "tipo_transporte": "virtual"})
    assert response.status_code == 400
    assert "El valor debe estar entre" in response.text

def test_recharge_invalid_value_high(monkeypatch):
    monkeypatch.setattr("src.backend.app.api.routes.payment_cud_service.controller.get_by_id", lambda cls, id: Card(id=id, balance=1000))
    
    response = client.post("/payment/tarjeta/test-id/recarga", params={"valor": 200000, "tipo_transporte": "virtual"})
    assert response.status_code == 400
    assert "El valor debe estar entre" in response.text

def test_recharge_card_not_found(monkeypatch):
    monkeypatch.setattr("src.backend.app.api.routes.payment_cud_service.controller.get_by_id", lambda cls, id: None)
    
    response = client.post("/payment/tarjeta/test-id/recarga", params={"valor": 5000, "tipo_transporte": "virtual"})
    assert response.status_code == 404
    assert "Tarjeta no encontrada" in response.text

def test_use_card_not_found(monkeypatch):
    monkeypatch.setattr("src.backend.app.api.routes.payment_cud_service.controller.get_by_id", lambda cls, id: None)
    
    response = client.post("/tarjeta/test-id/uso", params={"valor": 5000, "tipo_transporte": "metro"})
    assert response.status_code == 404
    assert "Tarjeta no encontrada" in response.text

def test_use_insufficient_balance(monkeypatch):
    monkeypatch.setattr("src.backend.app.api.routes.payment_cud_service.controller.get_by_id", lambda cls, id: Card(id=id, balance=1000))
    
    response = client.post("/tarjeta/test-id/uso", params={"valor": 5000, "tipo_transporte": "metro"})
    assert response.status_code == 400
    assert "Saldo insuficiente" in response.text
