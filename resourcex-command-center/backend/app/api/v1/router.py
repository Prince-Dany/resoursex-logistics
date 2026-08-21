from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...core.security import bearer_scheme, create_access_token, decode_access_token, hash_password, verify_password
from ...models import MarketplaceOffer, Notification, Order, Resource, RiskSignal, Route, Simulation, Supplier, User
from ...schemas import DashboardOut, LoginRequest, NotificationOut, OfferOut, OrderCreate, OrderOut, OrderStatusUpdate, RiskOut, RouteOut, SearchResult, SimulationOut, SimulationRequest, SupplierOut, TokenOut, UserCreate, UserOut
from ...services.simulation import run_supply_simulation

router = APIRouter()


def not_found(code: str, message: str):
    raise HTTPException(status_code=404, detail={"code": code, "message": message})


def entity_uuid(value: str, code: str, message: str) -> UUID:
    try:
        return UUID(value)
    except ValueError:
        not_found(code, message)


def offer_out(row: tuple[MarketplaceOffer, Supplier, Resource]) -> OfferOut:
    offer, supplier, resource = row
    return OfferOut(id=offer.id, resource=resource.name, resource_unit=resource.unit, supplier=supplier.name, origin=offer.origin, quantity=offer.quantity, unit_price=float(offer.unit_price), delivery_min_days=offer.delivery_min_days, delivery_max_days=offer.delivery_max_days, risk_level=offer.risk_level, status=offer.status)


@router.post("/auth/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == payload.email.lower())):
        raise HTTPException(status_code=409, detail={"code": "EMAIL_ALREADY_REGISTERED", "message": "An account with this email already exists"})
    user = User(email=payload.email.lower(), full_name=payload.full_name, password_hash=hash_password(payload.password))
    db.add(user); db.commit(); db.refresh(user)
    return user


@router.post("/auth/login", response_model=TokenOut)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail={"code": "INVALID_CREDENTIALS", "message": "Email or password is incorrect"})
    return TokenOut(access_token=create_access_token(str(user.id)))


@router.get("/auth/me", response_model=UserOut)
def me(credentials=Depends(bearer_scheme), db: Session = Depends(get_db)):
    user = db.get(User, entity_uuid(decode_access_token(credentials), "USER_NOT_FOUND", "User was not found"))
    if not user: not_found("USER_NOT_FOUND", "User was not found")
    return user


@router.get("/dashboard", response_model=DashboardOut)
def dashboard(db: Session = Depends(get_db)):
    routes = db.scalars(select(Route)).all()
    signals = db.scalars(select(RiskSignal).where(RiskSignal.status == "open").order_by(RiskSignal.created_at.desc()).limit(3)).all()
    qualified_sources = db.scalar(select(func.count()).select_from(Supplier).where(Supplier.status == "qualified")) or 0
    active_orders = db.scalar(select(func.count()).select_from(Order).where(Order.status.in_(["requested", "confirmed", "in_transit"]))) or 0
    at_risk = sum(route.risk_level in {"Watch", "Elevated", "High"} for route in routes)
    return DashboardOut(resilience_score=max(0, 100 - at_risk * 7), active_orders=active_orders, at_risk_routes=at_risk, supplier_coverage=min(100, qualified_sources * 13), qualified_sources=qualified_sources, market_offer_count=db.scalar(select(func.count()).select_from(MarketplaceOffer).where(MarketplaceOffer.status == "available")) or 0, signals=signals)


@router.get("/marketplace/offers", response_model=list[OfferOut])
def list_offers(resource: str | None = None, db: Session = Depends(get_db)):
    query = select(MarketplaceOffer, Supplier, Resource).join(Supplier).join(Resource).where(MarketplaceOffer.status == "available")
    if resource: query = query.where(Resource.name.ilike(f"%{resource}%"))
    return [offer_out(row) for row in db.execute(query.order_by(MarketplaceOffer.unit_price)).all()]


@router.get("/marketplace/offers/{offer_id}", response_model=OfferOut)
def get_offer(offer_id: str, db: Session = Depends(get_db)):
    offer_uuid = entity_uuid(offer_id, "OFFER_NOT_FOUND", "Marketplace offer was not found")
    row = db.execute(select(MarketplaceOffer, Supplier, Resource).join(Supplier).join(Resource).where(MarketplaceOffer.id == offer_uuid)).first()
    if not row: not_found("OFFER_NOT_FOUND", "Marketplace offer was not found")
    return offer_out(row)


@router.get("/suppliers", response_model=list[SupplierOut])
def list_suppliers(db: Session = Depends(get_db)):
    return db.scalars(select(Supplier).order_by(Supplier.reliability_score.desc())).all()


@router.get("/routes", response_model=list[RouteOut])
def list_routes(db: Session = Depends(get_db)):
    return db.scalars(select(Route).order_by(Route.id)).all()


@router.get("/risk", response_model=list[RiskOut])
def list_risk(db: Session = Depends(get_db)):
    return db.scalars(select(RiskSignal).where(RiskSignal.status == "open").order_by(RiskSignal.score.desc())).all()


@router.get("/notifications", response_model=list[NotificationOut])
def list_notifications(db: Session = Depends(get_db)):
    return db.scalars(select(Notification).order_by(Notification.is_read, Notification.created_at.desc())).all()


@router.patch("/notifications/{notification_id}/read", response_model=NotificationOut)
def mark_notification_read(notification_id: str, db: Session = Depends(get_db)):
    notification = db.get(Notification, entity_uuid(notification_id, "NOTIFICATION_NOT_FOUND", "Notification was not found"))
    if not notification: not_found("NOTIFICATION_NOT_FOUND", "Notification was not found")
    notification.is_read = True; db.commit(); db.refresh(notification)
    return notification


@router.post("/simulations", response_model=SimulationOut, status_code=201)
def create_simulation(payload: SimulationRequest, db: Session = Depends(get_db)):
    at_risk = db.scalar(select(func.count()).select_from(Route).where(Route.risk_level.in_(["Watch", "Elevated", "High"]))) or 0
    results = run_supply_simulation(payload.disruption_percent, payload.duration_days, at_risk)
    simulation = Simulation(scenario_type=payload.scenario_type, parameters=payload.model_dump(), results=results)
    db.add(simulation); db.commit(); db.refresh(simulation)
    return simulation


@router.get("/orders", response_model=list[OrderOut])
def list_orders(credentials=Depends(bearer_scheme), db: Session = Depends(get_db)):
    user_id = entity_uuid(decode_access_token(credentials), "USER_NOT_FOUND", "User was not found")
    return db.scalars(select(Order).where(Order.user_id == user_id).order_by(Order.created_at.desc())).all()


@router.post("/orders", response_model=OrderOut, status_code=201)
def create_order(payload: OrderCreate, credentials=Depends(bearer_scheme), db: Session = Depends(get_db)):
    offer = db.get(MarketplaceOffer, payload.offer_id)
    if not offer: not_found("OFFER_NOT_FOUND", "Marketplace offer was not found")
    if offer.status != "available" or payload.quantity > offer.quantity:
        raise HTTPException(status_code=422, detail={"code": "ORDER_NOT_AVAILABLE", "message": "Requested quantity is not available"})
    user_id = entity_uuid(decode_access_token(credentials), "USER_NOT_FOUND", "User was not found")
    order = Order(user_id=user_id, offer_id=offer.id, quantity=payload.quantity, delivery_location=payload.delivery_location)
    db.add(order); db.commit(); db.refresh(order)
    return order


@router.patch("/orders/{order_id}/status", response_model=OrderOut)
def update_order_status(order_id: str, payload: OrderStatusUpdate, credentials=Depends(bearer_scheme), db: Session = Depends(get_db)):
    user_id = entity_uuid(decode_access_token(credentials), "USER_NOT_FOUND", "User was not found")
    order = db.get(Order, entity_uuid(order_id, "ORDER_NOT_FOUND", "Order was not found"))
    if not order or order.user_id != user_id: not_found("ORDER_NOT_FOUND", "Order was not found")
    valid_transitions = {"requested": {"confirmed", "cancelled"}, "confirmed": {"in_transit", "cancelled"}, "in_transit": {"delivered"}, "delivered": set(), "cancelled": set()}
    if payload.status not in valid_transitions.get(order.status, set()):
        raise HTTPException(status_code=422, detail={"code": "INVALID_ORDER_TRANSITION", "message": f"Cannot change an order from {order.status} to {payload.status}"})
    order.status = payload.status; db.commit(); db.refresh(order)
    return order


@router.get("/search", response_model=list[SearchResult])
def search(q: str, db: Session = Depends(get_db)):
    term = q.strip()
    if len(term) < 2: return []
    pattern = f"%{term}%"; results: list[SearchResult] = []
    results += [SearchResult(type="supplier", id=str(s.id), title=s.name, subtitle=f"{s.location} · reliability {s.reliability_score}") for s in db.scalars(select(Supplier).where(or_(Supplier.name.ilike(pattern), Supplier.location.ilike(pattern))).limit(5))]
    results += [SearchResult(type="resource", id=str(r.id), title=r.name, subtitle=f"{r.grade or 'Standard'} · {r.unit}") for r in db.scalars(select(Resource).where(Resource.name.ilike(pattern)).limit(5))]
    results += [SearchResult(type="route", id=r.id, title=r.name, subtitle=f"{r.progress}% complete · {r.risk_level} risk") for r in db.scalars(select(Route).where(Route.name.ilike(pattern)).limit(5))]
    results += [SearchResult(type="risk", id=str(r.id), title=r.title, subtitle=r.description) for r in db.scalars(select(RiskSignal).where(RiskSignal.title.ilike(pattern)).limit(5))]
    return results[:10]
