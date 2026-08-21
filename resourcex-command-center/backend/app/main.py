from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.router import router
from .core.config import get_settings
from .core.database import Base, SessionLocal, engine
from .services.seed import seed_database
from . import models  # noqa: F401 - registers metadata


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Development convenience; production deployments should use Alembic before startup.
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_database(db)
    yield


app = FastAPI(title="ResourceX API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=get_settings().cors_origin_list, allow_credentials=True, allow_methods=["GET", "POST", "PATCH"], allow_headers=["Authorization", "Content-Type"])
app.include_router(router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
