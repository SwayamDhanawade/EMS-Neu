from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models  # noqa: F401
from app.api.employees import router as employees_router
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Employee Management System",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(employees_router, prefix="/employees", tags=["employees"])


@app.get("/health")
def health():
    return {"status": "ok"}
