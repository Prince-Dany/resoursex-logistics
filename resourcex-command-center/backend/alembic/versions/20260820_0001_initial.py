"""initial resourcex schema

Revision ID: 20260820_0001
Revises:
Create Date: 2026-08-20
"""
from alembic import op
import sqlalchemy as sa

revision = "20260820_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("email", sa.String(320), nullable=False), sa.Column("full_name", sa.String(120), nullable=False), sa.Column("password_hash", sa.String(255), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("email"))
    op.create_index("ix_users_email", "users", ["email"])
    op.create_table("resources", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("name", sa.String(120), nullable=False), sa.Column("unit", sa.String(24), nullable=False), sa.Column("grade", sa.String(80)), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.UniqueConstraint("name"))
    op.create_index("ix_resources_name", "resources", ["name"])
    op.create_table("suppliers", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("name", sa.String(160), nullable=False), sa.Column("location", sa.String(160), nullable=False), sa.Column("reliability_score", sa.Integer(), nullable=False), sa.Column("capacity", sa.Float(), nullable=False), sa.Column("risk_level", sa.String(16), nullable=False), sa.Column("status", sa.String(24), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.CheckConstraint("reliability_score BETWEEN 0 AND 100"), sa.UniqueConstraint("name"))
    op.create_index("ix_suppliers_name", "suppliers", ["name"])
    op.create_table("marketplace_offers", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("supplier_id", sa.Uuid(), sa.ForeignKey("suppliers.id"), nullable=False), sa.Column("resource_id", sa.Uuid(), sa.ForeignKey("resources.id"), nullable=False), sa.Column("origin", sa.String(160), nullable=False), sa.Column("quantity", sa.Float(), nullable=False), sa.Column("unit_price", sa.Numeric(12, 2), nullable=False), sa.Column("delivery_min_days", sa.Integer(), nullable=False), sa.Column("delivery_max_days", sa.Integer(), nullable=False), sa.Column("risk_level", sa.String(16), nullable=False), sa.Column("status", sa.String(24), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.CheckConstraint("quantity > 0"), sa.CheckConstraint("delivery_min_days >= 0 AND delivery_max_days >= delivery_min_days"))
    op.create_index("ix_marketplace_offers_supplier_id", "marketplace_offers", ["supplier_id"]); op.create_index("ix_marketplace_offers_resource_id", "marketplace_offers", ["resource_id"]); op.create_index("ix_marketplace_offers_status", "marketplace_offers", ["status"]); op.create_index("ix_offers_supplier_resource", "marketplace_offers", ["supplier_id", "resource_id"])
    op.create_table("routes", sa.Column("id", sa.String(24), primary_key=True), sa.Column("name", sa.String(180), nullable=False), sa.Column("resource_id", sa.Uuid(), sa.ForeignKey("resources.id"), nullable=False), sa.Column("origin", sa.String(160), nullable=False), sa.Column("destination", sa.String(160), nullable=False), sa.Column("origin_lat", sa.Float(), nullable=False), sa.Column("origin_lng", sa.Float(), nullable=False), sa.Column("destination_lat", sa.Float(), nullable=False), sa.Column("destination_lng", sa.Float(), nullable=False), sa.Column("progress", sa.Integer(), nullable=False), sa.Column("eta_days", sa.Integer(), nullable=False), sa.Column("risk_level", sa.String(16), nullable=False), sa.Column("status", sa.String(24), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.CheckConstraint("progress BETWEEN 0 AND 100"))
    op.create_index("ix_routes_resource_id", "routes", ["resource_id"])
    op.create_table("orders", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("user_id", sa.Uuid(), sa.ForeignKey("users.id"), nullable=False), sa.Column("offer_id", sa.Uuid(), sa.ForeignKey("marketplace_offers.id"), nullable=False), sa.Column("quantity", sa.Float(), nullable=False), sa.Column("delivery_location", sa.String(160), nullable=False), sa.Column("status", sa.String(24), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False), sa.CheckConstraint("quantity > 0"))
    op.create_index("ix_orders_user_id", "orders", ["user_id"]); op.create_index("ix_orders_offer_id", "orders", ["offer_id"]); op.create_index("ix_orders_status", "orders", ["status"])
    op.create_table("risk_signals", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("route_id", sa.String(24), sa.ForeignKey("routes.id")), sa.Column("supplier_id", sa.Uuid(), sa.ForeignKey("suppliers.id")), sa.Column("title", sa.String(180), nullable=False), sa.Column("description", sa.Text(), nullable=False), sa.Column("severity", sa.String(16), nullable=False), sa.Column("category", sa.String(80), nullable=False), sa.Column("score", sa.Integer(), nullable=False), sa.Column("status", sa.String(24), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_risk_signals_route_id", "risk_signals", ["route_id"]); op.create_index("ix_risk_signals_supplier_id", "risk_signals", ["supplier_id"]); op.create_index("ix_risk_signals_status", "risk_signals", ["status"])
    op.create_table("notifications", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("title", sa.String(180), nullable=False), sa.Column("body", sa.Text(), nullable=False), sa.Column("severity", sa.String(16), nullable=False), sa.Column("is_read", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))
    op.create_index("ix_notifications_is_read", "notifications", ["is_read"])
    op.create_table("simulations", sa.Column("id", sa.Uuid(), primary_key=True), sa.Column("scenario_type", sa.String(80), nullable=False), sa.Column("parameters", sa.JSON(), nullable=False), sa.Column("status", sa.String(24), nullable=False), sa.Column("results", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False))


def downgrade() -> None:
    for table in ["simulations", "notifications", "risk_signals", "orders", "routes", "marketplace_offers", "suppliers", "resources", "users"]:
        op.drop_table(table)
