from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: str
    date_joined: date


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    date_joined: Optional[date] = None


class EmployeeResponse(EmployeeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
