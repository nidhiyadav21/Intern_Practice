from sqlalchemy.orm import Session
import models, schemas              #exceptions

def get_employees(db: Session):
    return db.query(models.Employee).all()

def get_employee_by_id(db: Session, emp_id: int):
    return db.query(models.Employee).filter(models.Employee.id == emp_id).first()

def create_employee(db: Session, employee: schemas.EmployeeCreate):
    db_employee = models.Employee(**employee.model_dump())  #dump - Converts the Pydantic Object into a dictionary and "unpacks" it
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

def update_employee(db: Session, emp_id: int, updates: schemas.EmployeeUpdate):
    db_query = db.query(models.Employee).filter(models.Employee.id == emp_id)
    if not db_query.first():
        return None
    db_query.update(updates.model_dump(exclude_unset=True)) #It ensures that if the user only sends a new salary,you don't overwrite the name and email with none
    db.commit()
    return db_query.first()

def delete_employee(db: Session, emp_id: int):
    db_employee = db.query(models.Employee).filter(models.Employee.id == emp_id).first()
    if db_employee:
        db.delete(db_employee)
        db.commit()
    return db_employee
