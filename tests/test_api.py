from datetime import date
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.api.employees import get_employee_service
from app.core.exceptions import DuplicateEmailError, EmployeeNotFoundError
from app.main import app


@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def mock_service():
    mock = MagicMock()
    app.dependency_overrides[get_employee_service] = lambda: mock
    return mock


@pytest.fixture
def client():
    return TestClient(app, raise_server_exceptions=False)


class TestCreateEmployee:
    def test_returns_201(self, client, mock_service):
        mock_service.create_employee.return_value = {
            "id": 1, "name": "Alice", "email": "a@b.com",
            "department": "Eng", "date_joined": "2024-01-15",
        }

        resp = client.post("/employees", json={
            "name": "Alice", "email": "a@b.com",
            "department": "Eng", "date_joined": "2024-01-15",
        })

        assert resp.status_code == 201
        assert resp.json()["id"] == 1

    def test_returns_409_on_duplicate_email(self, client, mock_service):
        mock_service.create_employee.side_effect = DuplicateEmailError("a@b.com")

        resp = client.post("/employees", json={
            "name": "Alice", "email": "a@b.com",
            "department": "Eng", "date_joined": "2024-01-15",
        })

        assert resp.status_code == 409
        assert "already exists" in resp.json()["detail"]


class TestListEmployees:
    def test_returns_200(self, client, mock_service):
        mock_service.get_all_employees.return_value = []

        resp = client.get("/employees")

        assert resp.status_code == 200
        assert resp.json() == []


class TestGetEmployee:
    def test_returns_200_when_found(self, client, mock_service):
        mock_service.get_employee_by_id.return_value = {
            "id": 1, "name": "Alice", "email": "a@b.com",
            "department": "Eng", "date_joined": "2024-01-15",
        }

        resp = client.get("/employees/1")

        assert resp.status_code == 200
        assert resp.json()["id"] == 1

    def test_returns_404_when_missing(self, client, mock_service):
        mock_service.get_employee_by_id.side_effect = EmployeeNotFoundError(999)

        resp = client.get("/employees/999")

        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"]


class TestUpdateEmployee:
    def test_returns_200(self, client, mock_service):
        mock_service.update_employee.return_value = {
            "id": 1, "name": "Alice B.", "email": "a@b.com",
            "department": "Eng", "date_joined": "2024-01-15",
        }

        resp = client.put("/employees/1", json={"name": "Alice B."})

        assert resp.status_code == 200
        assert resp.json()["name"] == "Alice B."

    def test_returns_409_on_duplicate_email(self, client, mock_service):
        mock_service.update_employee.side_effect = DuplicateEmailError("taken@b.com")

        resp = client.put("/employees/1", json={"email": "taken@b.com"})

        assert resp.status_code == 409
        assert "already exists" in resp.json()["detail"]

    def test_returns_404_when_missing(self, client, mock_service):
        mock_service.update_employee.side_effect = EmployeeNotFoundError(999)

        resp = client.put("/employees/999", json={"name": "Nope"})

        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"]


class TestDeleteEmployee:
    def test_returns_204(self, client, mock_service):
        mock_service.delete_employee.return_value = None

        resp = client.delete("/employees/1")

        assert resp.status_code == 204
        assert resp.content == b""

    def test_returns_404_when_missing(self, client, mock_service):
        mock_service.delete_employee.side_effect = EmployeeNotFoundError(999)

        resp = client.delete("/employees/999")

        assert resp.status_code == 404
        assert "not found" in resp.json()["detail"]
