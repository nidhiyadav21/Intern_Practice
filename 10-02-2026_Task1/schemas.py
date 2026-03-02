from pydantic import BaseModel, EmailStr, Field  # EmailStr - validates if a string is a real email format
from typing import Optional

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: str
    salary: float = Field(gt=0, description="Salary must be greater than 0")
    phone_number: str
    is_active: bool = True

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = Field(None, gt=0)
    phone_number: Optional[str] = None

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        from_attributes = True # Allows Pydantic to read SQLAlchemy models
