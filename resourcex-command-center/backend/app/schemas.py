from datetime import datetime
from typing import Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=12, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(ORMModel):
    id: UUID
    email: EmailStr
    full_name: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class OfferOut(BaseModel):
    id: UUID
    resource: str
    resource_unit: str
    supplier: str
    origin: str
    quantity: float
    unit_price: float
    delivery_min_days: int
    delivery_max_days: int
    risk_level: str
    status: str


class SupplierOut(ORMModel):
    id: UUID
    name: str
    location: str
    reliability_score: int
    capacity: float
    risk_level: str
    status: str


class RouteOut(ORMModel):
    id: str
    name: str
    origin: str
    destination: str
    progress: int
    eta_days: int
    risk_level: str
    status: str


class RiskOut(ORMModel):
    id: UUID
    title: str
    description: str
    severity: str
    category: str
    score: int
    status: str
    created_at: datetime


class NotificationOut(ORMModel):
    id: UUID
    title: str
    body: str
    severity: str
    is_read: bool
    created_at: datetime


class DashboardOut(BaseModel):
    resilience_score: int
    active_orders: int
    at_risk_routes: int
    supplier_coverage: int
    qualified_sources: int
    market_offer_count: int
    signals: list[RiskOut]


class SimulationRequest(BaseModel):
    scenario_type: Literal["supplier_export_fall", "route_disruption"] = "supplier_export_fall"
    disruption_percent: int = Field(default=40, ge=1, le=100)
    duration_days: int = Field(default=15, ge=1, le=365)
    resource: str = Field(default="Natural gas", min_length=2, max_length=120)
    route_id: str | None = None


class SimulationOut(ORMModel):
    id: UUID
    status: str
    results: dict
    created_at: datetime


class OrderCreate(BaseModel):
    offer_id: UUID
    quantity: float = Field(gt=0)
    delivery_location: str = Field(min_length=2, max_length=160)


class OrderOut(ORMModel):
    id: UUID
    offer_id: UUID
    quantity: float
    delivery_location: str
    status: str
    created_at: datetime


class OrderStatusUpdate(BaseModel):
    status: Literal["confirmed", "in_transit", "delivered", "cancelled"]


class SearchResult(BaseModel):
    type: Literal["supplier", "resource", "route", "risk"]
    id: str
    title: str
    subtitle: str
