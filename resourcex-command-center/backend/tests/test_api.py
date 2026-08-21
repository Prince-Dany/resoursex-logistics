import os
os.environ["DATABASE_URL"] = "sqlite:///./test_resourcex.db"
os.environ["JWT_SECRET"] = "test-secret-with-at-least-thirty-two-bytes"

from fastapi.testclient import TestClient
from app.core.database import Base, engine
from app.main import app


def setup_module():
    Base.metadata.drop_all(bind=engine)


def test_public_data_and_simulation():
    with TestClient(app) as client:
        assert client.get("/api/v1/dashboard").status_code == 200
        offers = client.get("/api/v1/marketplace/offers").json()
        assert len(offers) >= 3 and offers[0]["supplier"]
        assert len(client.get("/api/v1/suppliers").json()) >= 3
        assert len(client.get("/api/v1/routes").json()) == 3
        response = client.post("/api/v1/simulations", json={"scenario_type": "supplier_export_fall", "disruption_percent": 40, "duration_days": 15, "resource": "Natural gas"})
        assert response.status_code == 201
        assert response.json()["results"]["coverage_change_percent"] < 0


def test_auth_and_orders():
    with TestClient(app) as client:
        assert client.post("/api/v1/auth/register", json={"email": "operator@example.com", "full_name": "Operator", "password": "safe-password-123"}).status_code == 201
        login = client.post("/api/v1/auth/login", json={"email": "operator@example.com", "password": "safe-password-123"})
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        assert client.get("/api/v1/auth/me", headers=headers).status_code == 200
        assert client.get("/api/v1/orders").status_code == 401
        offer = client.get("/api/v1/marketplace/offers").json()[0]
        assert client.post("/api/v1/orders", headers=headers, json={"offer_id": offer["id"], "quantity": 1000, "delivery_location": "Chennai"}).status_code == 201
        order = client.get("/api/v1/orders", headers=headers).json()[0]
        assert client.patch(f"/api/v1/orders/{order['id']}/status", headers=headers, json={"status": "delivered"}).status_code == 422
        assert client.post("/api/v1/orders", headers=headers, json={"offer_id": offer["id"], "quantity": 999999, "delivery_location": "Chennai"}).status_code == 422


def test_validation_not_found_notifications_and_search():
    with TestClient(app) as client:
        assert client.post("/api/v1/simulations", json={"disruption_percent": 101}).status_code == 422
        assert client.get("/api/v1/marketplace/offers/not-a-uuid").status_code == 404
        notification = client.get("/api/v1/notifications").json()[0]
        assert client.patch(f"/api/v1/notifications/{notification['id']}/read").json()["is_read"] is True
        assert client.get("/api/v1/search", params={"q": "Atlas"}).json()[0]["type"] == "supplier"
