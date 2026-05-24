from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.employee import Employee


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, employee_data: dict) -> Employee:
        employee = Employee(**employee_data)
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def get_all(self) -> list[Employee]:
        stmt = select(Employee).order_by(Employee.id)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, employee_id: int) -> Employee | None:
        stmt = select(Employee).where(Employee.id == employee_id)
        return self.db.scalars(stmt).one_or_none()

    def get_by_email(self, email: str) -> Employee | None:
        stmt = select(Employee).where(Employee.email == email)
        return self.db.scalars(stmt).one_or_none()

    def update(self, employee: Employee, update_data: dict) -> Employee:
        for field, value in update_data.items():
            setattr(employee, field, value)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def delete(self, employee: Employee) -> None:
        self.db.delete(employee)
        self.db.commit()
