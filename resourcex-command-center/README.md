# ResourceX Command Center

ResourceX is a React command-center frontend backed by a FastAPI modular monolith and PostgreSQL. The dashboard, qualified marketplace, supplier comparison, route register, notifications, command search, and disruption simulator use the API instead of frontend fixtures.

## Requirements

- Node.js 20+ and pnpm 10+
- Python 3.12+
- PostgreSQL 16+

## Configuration

Create `backend/.env` from `backend/.env.example`, then set a strong `JWT_SECRET` and a PostgreSQL `DATABASE_URL`. Create a root `.env` from `.env.example` for the frontend API base URL.

Example local database setup:

```sql
CREATE USER resourcex WITH PASSWORD 'change-this-password';
CREATE DATABASE resourcex OWNER resourcex;
```

## Run locally

In one terminal, set up the backend and run the migration. The migration creates the production schema; starting the application adds only the deterministic development seed data when the database is empty.

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

In a second terminal:

```powershell
pnpm install
pnpm dev
```

The frontend runs on `http://localhost:3000`, the API on `http://localhost:8000/api/v1`, and interactive API documentation is at `http://localhost:8000/docs`.

## API overview

- `POST /api/v1/auth/register`, `POST /api/v1/auth/login`, `GET /api/v1/auth/me` — JWT account flows.
- `GET /api/v1/dashboard` — calculated command-center metrics and current risk signals.
- `GET /api/v1/marketplace/offers`, `GET /api/v1/marketplace/offers/{id}` — available qualified supply.
- `GET /api/v1/suppliers`, `GET /api/v1/routes`, `GET /api/v1/risk` — live operational data.
- `GET /api/v1/notifications`, `PATCH /api/v1/notifications/{id}/read` — notification state.
- `POST /api/v1/simulations` — deterministic, explainable disruption scenario result.
- `GET /api/v1/search?q=` — normalized supplier, resource, route, and risk search.
- `GET|POST /api/v1/orders` — authenticated orders (Bearer access token required).

Read-only operational data and simulations are public in this version so the existing no-login UI stays usable. User identity and order mutations are JWT-protected. Production deployments should restrict read access according to the organization’s tenancy model.

## Tests and checks

```powershell
cd backend
pytest

cd ..
pnpm check
pnpm build
```

The backend tests use a temporary SQLite database for speed and exercise authentication, unauthorized access, validation, data endpoints, notifications, search, simulations, and invalid order quantities. PostgreSQL remains the configured runtime database.

## Architecture and schema

`backend/app` contains configuration/security/database infrastructure, SQLAlchemy models, Pydantic contracts, API routing, and deterministic simulation/seed services. The initial Alembic migration creates users, resources, suppliers, marketplace offers, orders, routes, risk signals, notifications, and simulations. UUID keys, indexes, timestamps, foreign keys, and core validation constraints are included.
