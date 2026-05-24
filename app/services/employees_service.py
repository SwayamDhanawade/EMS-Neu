from app.core.exceptions import DuplicateEmailError, EmployeeNotFoundError
from app.repositories.employees_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    def create_employee(self, employee_create: EmployeeCreate):
        existing = self.repository.get_by_email(employee_create.email)
        if existing:
            raise DuplicateEmailError(employee_create.email)
        return self.repository.create(employee_create.model_dump())

    def get_all_employees(self):
        return self.repository.get_all()

    def get_employee_by_id(self, employee_id: int):
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(employee_id)
        return employee

    def update_employee(self, employee_id: int, employee_update: EmployeeUpdate):
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(employee_id)

        update_data = employee_update.model_dump(exclude_unset=True)

        if "email" in update_data:
            existing = self.repository.get_by_email(update_data["email"])
            if existing and existing.id != employee_id:
                raise DuplicateEmailError(update_data["email"])

        if not update_data:
            return employee

        return self.repository.update(employee, update_data)

    def delete_employee(self, employee_id: int):
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise EmployeeNotFoundError(employee_id)
        self.repository.delete(employee)
