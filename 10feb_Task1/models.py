from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Employee(Base):
    __tablename__ = "Employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    department = Column(String(50))
    salary = Column(Float)
    phone_number = Column(String(20))
    is_active = Column(Boolean, default=True)
