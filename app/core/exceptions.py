class ServiceError(Exception):
    pass


class EmployeeNotFoundError(ServiceError):
    def __init__(self, employee_id: int):
        self.employee_id = employee_id
        super().__init__(f"Employee with id {employee_id} not found")


class DuplicateEmailError(ServiceError):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Employee with email {email} already exists")
