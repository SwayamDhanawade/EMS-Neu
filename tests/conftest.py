from datetime import date
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import get_db
from app.main import app
from app.models.base import Base
from app.repositories.employees_repository import EmployeeRepository
from app.services.employees_service import EmployeeService


@pytest.fixture
def db_session():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def employee_repository(db_session):
    return EmployeeRepository(db_session)


@pytest.fixture
def sample_employee_data():
    return {
        "name": "Alice",
        "email": "alice@example.com",
        "department": "Engineering",
        "date_joined": date(2024, 1, 15),
    }


@pytest.fixture
def sample_employee(employee_repository, sample_employee_data):
    return employee_repository.create(sample_employee_data)


@pytest.fixture
def mock_repo():
    return MagicMock(spec=EmployeeRepository)


@pytest.fixture
def employee_service(mock_repo):
    return EmployeeService(mock_repo)


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=False)
