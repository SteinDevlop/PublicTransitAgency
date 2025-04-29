from fastapi.testclient import TestClient
from backend.app.api.routes.payment_query_service import app

client = TestClient(app)

def test_get_payment_schema():
    response = client.get("/schema/payments")
    assert response.status_code == 200
    schema = response.json()
    assert "fields" in schema
    assert any(f["name"] == "id" for f in schema["fields"])

def test_get_all_payments():
    response = client.get("/payments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_payment_not_found():
    response = client.get("/payments/nonexistent-id")
    assert response.status_code == 404

def test_get_payments_by_card_not_found():
    response = client.get("/payments/card/nonexistent-card")
    assert response.status_code == 404
