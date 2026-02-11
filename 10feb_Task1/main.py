from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, schemas, models, database

# # --- ADD THIS LINE HERE ---
# # This creates the tables in the DB if they don't exist
# models.Base.metadata.create_all(bind=database.engine)
# # --------------------------

app = FastAPI()

@app.get("/employees", response_model=list[schemas.EmployeeResponse])
def read_employees(db: Session = Depends(database.get_db)):
    return crud.get_employees(db)

@app.get("/employees/{id}", response_model=schemas.EmployeeResponse)
def read_employee(id: int, db: Session = Depends(database.get_db)):
    employee = crud.get_employee_by_id(db, id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.post("/employees", response_model=schemas.EmployeeResponse)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(database.get_db)):
    # Error handling for duplicate email
    existing = db.query(models.Employee).filter(models.Employee.email == employee.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already exists")
    return crud.create_employee(db, employee)


# Update an existing employee (PUT)
@app.put("/employees/{id}", response_model=schemas.EmployeeResponse)
def update_employee(id: int, updated_data: schemas.EmployeeUpdate, db: Session = Depends(database.get_db)):
    employee = crud.update_employee(db, id, updated_data)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


# Activate/Deactivate employee (PATCH)
@app.patch("/employees/{id}/status", response_model=schemas.EmployeeResponse)
def toggle_status(id: int, db: Session = Depends(database.get_db)):
    employee = crud.get_employee_by_id(db, id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee.is_active = not employee.is_active
    db.commit()
    db.refresh(employee)
    return employee


# Delete an employee (DELETE)
@app.delete("/employees/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employee(id: int, db: Session = Depends(database.get_db)):
    success = crud.delete_employee(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
    return None


