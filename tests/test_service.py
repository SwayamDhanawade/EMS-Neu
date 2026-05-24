from datetime import date
from unittest.mock import MagicMock

import pytest

from app.core.exceptions import DuplicateEmailError, EmployeeNotFoundError
from app.models.employee import Employee
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


@pytest.fixture
def employee_create_payload():
    return EmployeeCreate(
        name="Alice",
        email="alice@example.com",
        department="Engineering",
        date_joined=date(2024, 1, 15),
    )


@pytest.fixture
def fake_employee():
    return Employee(
        id=1,
        name="Alice",
        email="alice@example.com",
        department="Engineering",
        date_joined=date(2024, 1, 15),
    )


class TestCreateEmployee:
    def test_succeeds_when_email_unique(self, employee_service, mock_repo, employee_create_payload, fake_employee):
        mock_repo.get_by_email.return_value = None
        mock_repo.create.return_value = fake_employee

        result = employee_service.create_employee(employee_create_payload)

        assert result == fake_employee
        mock_repo.get_by_email.assert_called_once_with("alice@example.com")
        mock_repo.create.assert_called_once()

    def test_raises_duplicate_email_when_email_exists(self, employee_service, mock_repo, employee_create_payload, fake_employee):
        mock_repo.get_by_email.return_value = fake_employee

        with pytest.raises(DuplicateEmailError):
            employee_service.create_employee(employee_create_payload)

        mock_repo.create.assert_not_called()


class TestGetAllEmployees:
    def test_delegates_to_repository(self, employee_service, mock_repo, fake_employee):
        mock_repo.get_all.return_value = [fake_employee]

        result = employee_service.get_all_employees()

        assert result == [fake_employee]
        mock_repo.get_all.assert_called_once()


class TestGetEmployeeById:
    def test_returns_employee_when_found(self, employee_service, mock_repo, fake_employee):
        mock_repo.get_by_id.return_value = fake_employee

        result = employee_service.get_employee_by_id(1)

        assert result == fake_employee

    def test_raises_not_found_when_missing(self, employee_service, mock_repo):
        mock_repo.get_by_id.return_value = None

        with pytest.raises(EmployeeNotFoundError):
            employee_service.get_employee_by_id(999)


class TestUpdateEmployee:
    def test_succeeds_with_partial_fields(self, employee_service, mock_repo, fake_employee):
        mock_repo.get_by_id.return_value = fake_employee
        mock_repo.get_by_email.return_value = None
        mock_repo.update.return_value = fake_employee
        update = EmployeeUpdate(name="Alice B.")

        result = employee_service.update_employee(1, update)

        assert result == fake_employee
        mock_repo.update.assert_called_once()

    def test_raises_not_found_when_missing(self, employee_service, mock_repo):
        mock_repo.get_by_id.return_value = None
        update = EmployeeUpdate(name="Bob")

        with pytest.raises(EmployeeNotFoundError):
            employee_service.update_employee(999, update)

        mock_repo.update.assert_not_called()

    def test_raises_duplicate_email_when_email_taken(self, employee_service, mock_repo, fake_employee):
        other = Employee(id=2, name="Bob", email="taken@example.com", department="Sales", date_joined=date(2024, 3, 1))
        mock_repo.get_by_id.return_value = fake_employee
        mock_repo.get_by_email.return_value = other
        update = EmployeeUpdate(email="taken@example.com")

        with pytest.raises(DuplicateEmailError):
            employee_service.update_employee(1, update)

        mock_repo.update.assert_not_called()

    def test_returns_unchanged_when_empty_payload(self, employee_service, mock_repo, fake_employee):
        mock_repo.get_by_id.return_value = fake_employee
        update = EmployeeUpdate()

        result = employee_service.update_employee(1, update)

        assert result == fake_employee
        mock_repo.update.assert_not_called()

    def test_allows_email_update_to_self(self, employee_service, mock_repo, fake_employee):
        mock_repo.get_by_id.return_value = fake_employee
        mock_repo.get_by_email.return_value = fake_employee
        mock_repo.update.return_value = fake_employee
        update = EmployeeUpdate(email="alice@example.com")

        result = employee_service.update_employee(1, update)

        assert result == fake_employee
        mock_repo.update.assert_called_once()


class TestDeleteEmployee:
    def test_deletes_when_found(self, employee_service, mock_repo, fake_employee):
        mock_repo.get_by_id.return_value = fake_employee

        employee_service.delete_employee(1)

        mock_repo.delete.assert_called_once_with(fake_employee)

    def test_raises_not_found_when_missing(self, employee_service, mock_repo):
        mock_repo.get_by_id.return_value = None

        with pytest.raises(EmployeeNotFoundError):
            employee_service.delete_employee(999)

        mock_repo.delete.assert_not_called()
