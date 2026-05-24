from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import app.models  # noqa: F401
from app.api.employees import router as employees_router
from app.core.database import init_db
from app.core.exceptions import DuplicateEmailError, EmployeeNotFoundError


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Employee Management System",
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(EmployeeNotFoundError)
def employee_not_found_handler(request: Request, exc: EmployeeNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(DuplicateEmailError)
def duplicate_email_handler(request: Request, exc: DuplicateEmailError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


app.include_router(employees_router, prefix="/employees", tags=["employees"])


@app.get("/health")
def health():
    return {"status": "ok"}
