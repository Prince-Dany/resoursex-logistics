import uuid
from datetime import datetime, timezone
from sqlalchemy import Boolean, CheckConstraint, DateTime, Float, ForeignKey, Index, Integer, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .core.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Timestamped:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)


class User(Timestamped, Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    password_hash: Mapped[str] = mapped_column(String(255))


class Resource(Timestamped, Base):
    __tablename__ = "resources"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    unit: Mapped[str] = mapped_column(String(24))
    grade: Mapped[str | None] = mapped_column(String(80))


class Supplier(Timestamped, Base):
    __tablename__ = "suppliers"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    location: Mapped[str] = mapped_column(String(160))
    reliability_score: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity: Mapped[float] = mapped_column(Float, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="qualified", nullable=False)
    __table_args__ = (CheckConstraint("reliability_score BETWEEN 0 AND 100"),)


class MarketplaceOffer(Timestamped, Base):
    __tablename__ = "marketplace_offers"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    supplier_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("suppliers.id"), index=True)
    resource_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("resources.id"), index=True)
    origin: Mapped[str] = mapped_column(String(160))
    quantity: Mapped[float] = mapped_column(Float)
    unit_price: Mapped[float] = mapped_column(Numeric(12, 2))
    delivery_min_days: Mapped[int] = mapped_column(Integer)
    delivery_max_days: Mapped[int] = mapped_column(Integer)
    risk_level: Mapped[str] = mapped_column(String(16))
    status: Mapped[str] = mapped_column(String(24), default="available", index=True)
    __table_args__ = (CheckConstraint("quantity > 0"), CheckConstraint("delivery_min_days >= 0 AND delivery_max_days >= delivery_min_days"))


class Order(Timestamped, Base):
    __tablename__ = "orders"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("marketplace_offers.id"), index=True)
    quantity: Mapped[float] = mapped_column(Float)
    delivery_location: Mapped[str] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(24), default="requested", index=True)
    __table_args__ = (CheckConstraint("quantity > 0"),)


class Route(Timestamped, Base):
    __tablename__ = "routes"
    id: Mapped[str] = mapped_column(String(24), primary_key=True)
    name: Mapped[str] = mapped_column(String(180))
    resource_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("resources.id"), index=True)
    origin: Mapped[str] = mapped_column(String(160))
    destination: Mapped[str] = mapped_column(String(160))
    origin_lat: Mapped[float] = mapped_column(Float)
    origin_lng: Mapped[float] = mapped_column(Float)
    destination_lat: Mapped[float] = mapped_column(Float)
    destination_lng: Mapped[float] = mapped_column(Float)
    progress: Mapped[int] = mapped_column(Integer)
    eta_days: Mapped[int] = mapped_column(Integer)
    risk_level: Mapped[str] = mapped_column(String(16))
    status: Mapped[str] = mapped_column(String(24), default="in_transit")
    __table_args__ = (CheckConstraint("progress BETWEEN 0 AND 100"),)


class RiskSignal(Timestamped, Base):
    __tablename__ = "risk_signals"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    route_id: Mapped[str | None] = mapped_column(ForeignKey("routes.id"), index=True)
    supplier_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("suppliers.id"), index=True)
    title: Mapped[str] = mapped_column(String(180))
    description: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(16))
    category: Mapped[str] = mapped_column(String(80))
    score: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(24), default="open", index=True)


class Notification(Timestamped, Base):
    __tablename__ = "notifications"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(180))
    body: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(16))
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, index=True)


class Simulation(Timestamped, Base):
    __tablename__ = "simulations"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    scenario_type: Mapped[str] = mapped_column(String(80))
    parameters: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(24), default="completed")
    results: Mapped[dict] = mapped_column(JSON, default=dict)

Index("ix_offers_supplier_resource", MarketplaceOffer.supplier_id, MarketplaceOffer.resource_id)
