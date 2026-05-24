from datetime import date

import pytest

from app.models.employee import Employee


class TestCreate:
    def test_returns_employee_with_id(self, employee_repository, sample_employee_data):
        employee = employee_repository.create(sample_employee_data)

        assert employee.id is not None
        assert employee.name == "Alice"
        assert employee.email == "alice@example.com"
        assert employee.department == "Engineering"
        assert employee.date_joined == date(2024, 1, 15)

    def test_persists_to_database(self, employee_repository, sample_employee_data):
        employee_repository.create(sample_employee_data)
        all_employees = employee_repository.get_all()
        assert len(all_employees) == 1


class TestGetAll:
    def test_returns_ordered_by_id(self, employee_repository):
        e1 = employee_repository.create({
            "name": "A", "email": "a@a.com", "department": "X", "date_joined": date(2024, 1, 1),
        })
        e2 = employee_repository.create({
            "name": "B", "email": "b@b.com", "department": "Y", "date_joined": date(2024, 2, 1),
        })

        result = employee_repository.get_all()

        assert result == [e1, e2]

    def test_returns_empty_list_when_no_employees(self, employee_repository):
        assert employee_repository.get_all() == []


class TestGetById:
    def test_returns_employee_when_found(self, sample_employee, employee_repository):
        result = employee_repository.get_by_id(sample_employee.id)
        assert result is not None
        assert result.id == sample_employee.id
        assert result.name == sample_employee.name

    def test_returns_none_when_missing(self, employee_repository):
        assert employee_repository.get_by_id(999) is None


class TestGetByEmail:
    def test_returns_employee_when_found(self, sample_employee, employee_repository):
        result = employee_repository.get_by_email(sample_employee.email)
        assert result is not None
        assert result.email == sample_employee.email

    def test_returns_none_when_missing(self, employee_repository):
        assert employee_repository.get_by_email("nobody@example.com") is None


class TestUpdate:
    def test_changes_only_provided_fields(self, sample_employee, employee_repository):
        updated = employee_repository.update(sample_employee, {"department": "Product"})

        assert updated.department == "Product"
        assert updated.name == "Alice"
        assert updated.email == "alice@example.com"

    def test_returns_same_object(self, sample_employee, employee_repository):
        updated = employee_repository.update(sample_employee, {"name": "Alice B."})
        assert updated is sample_employee


class TestDelete:
    def test_removes_employee(self, sample_employee, employee_repository):
        employee_repository.delete(sample_employee)
        assert employee_repository.get_by_id(sample_employee.id) is None

    def test_succeeds_on_already_deleted(self, sample_employee, employee_repository):
        employee_repository.delete(sample_employee)
        employee_repository.delete(sample_employee)
        assert employee_repository.get_by_id(sample_employee.id) is None
