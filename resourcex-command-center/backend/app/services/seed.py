import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..models import MarketplaceOffer, Notification, Order, Resource, RiskSignal, Route, Supplier, User


def seed_database(db: Session) -> None:
    if db.scalar(select(Supplier.id).limit(1)):
        return
    gas = Resource(name="Natural gas", unit="MMBtu", grade="Grade A")
    coke = Resource(name="Petroleum coke", unit="MT", grade="Grade A")
    coal = Resource(name="Thermal coal", unit="MT", grade="Grade A")
    atlas = Supplier(name="Atlas Energy", location="Dahej, India", reliability_score=94, capacity=50000, risk_level="Low")
    gujarat = Supplier(name="Gujarat LNG", location="Hazira, India", reliability_score=91, capacity=36000, risk_level="Low")
    western = Supplier(name="Western Fuels", location="Mundra, India", reliability_score=88, capacity=25000, risk_level="Watch")
    coral = Supplier(name="Coral Minerals", location="Paradip, India", reliability_score=81, capacity=22000, risk_level="Elevated")
    sapphire = Supplier(name="Sapphire Commodities", location="Kandla, India", reliability_score=89, capacity=14000, risk_level="Low")
    eastern = Supplier(name="Eastern Minerals", location="Haldia, India", reliability_score=87, capacity=16000, risk_level="Watch")
    demo_user = User(id=uuid.UUID("00000000-0000-0000-0000-000000000001"), email="seeded-operations@resourcex.invalid", full_name="Seeded Operations", password_hash="!disabled-seed-account")
    db.add_all([gas, coke, coal, atlas, gujarat, western, coral, sapphire, eastern, demo_user]); db.flush()
    atlas_offer = MarketplaceOffer(supplier_id=atlas.id, resource_id=gas.id, origin="Dahej, IN", quantity=25000, unit_price=4820, delivery_min_days=10, delivery_max_days=15, risk_level="Low")
    gujarat_offer = MarketplaceOffer(supplier_id=gujarat.id, resource_id=gas.id, origin="Hazira, IN", quantity=18000, unit_price=4970, delivery_min_days=8, delivery_max_days=12, risk_level="Low")
    western_offer = MarketplaceOffer(supplier_id=western.id, resource_id=coke.id, origin="Mundra, IN", quantity=8500, unit_price=19440, delivery_min_days=7, delivery_max_days=11, risk_level="Watch")
    coral_offer = MarketplaceOffer(supplier_id=coral.id, resource_id=coal.id, origin="Paradip, IN", quantity=20000, unit_price=7160, delivery_min_days=12, delivery_max_days=18, risk_level="Elevated")
    db.add_all([atlas_offer, gujarat_offer, western_offer, coral_offer]); db.flush()
    db.add_all([Order(user_id=demo_user.id, offer_id=atlas_offer.id, quantity=500, delivery_location="Chennai", status="in_transit" if index < 9 else "confirmed") for index in range(12)])
    db.add_all([
        Route(id="AE-44", name="Atlas Energy → Chennai", resource_id=gas.id, origin="Oman", destination="Chennai", origin_lat=23.6, origin_lng=58.5, destination_lat=13.1, destination_lng=80.3, progress=68, eta_days=6, risk_level="Low"),
        Route(id="WF-19", name="Western Fuels → Hazira", resource_id=coke.id, origin="Mundra", destination="Hazira", origin_lat=22.8, origin_lng=69.7, destination_lat=21.1, destination_lng=72.6, progress=42, eta_days=8, risk_level="Watch"),
        Route(id="CM-08", name="Coral Minerals → Chennai", resource_id=coal.id, origin="Paradip", destination="Chennai", origin_lat=20.3, origin_lng=86.7, destination_lat=13.1, destination_lng=80.3, progress=24, eta_days=14, risk_level="Elevated"),
    ]); db.flush()
    db.add_all([
        RiskSignal(route_id="AE-44", supplier_id=atlas.id, title="Natural gas exposure increased", description="Oman corridor congestion extends delivery risk by 8%.", severity="high", category="congestion", score=12),
        RiskSignal(route_id="WF-19", supplier_id=western.id, title="Alternative supply is qualified", description="Gujarat capacity can cover 64% of the gap.", severity="medium", category="capacity", score=6),
        RiskSignal(supplier_id=atlas.id, title="Supplier document refreshed", description="Atlas Energy terminal certificate is current.", severity="low", category="compliance", score=1),
        Notification(title="Chennai corridor requires review", body="A risk signal is open for the Atlas Energy route.", severity="high"),
    ])
    db.commit()
