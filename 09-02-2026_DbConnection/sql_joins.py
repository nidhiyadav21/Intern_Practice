from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import declarative_base,relationship,sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Department(Base):
    __tablename__ = 'Departments'
    DeptID = Column(Integer, primary_key=True)
    DeptName = Column(String)

class Employee(Base):
    __tablename__ = 'Employees'
    EmployeeID = Column(Integer, primary_key=True)
    Name = Column(String)
    DeptID = Column(Integer, ForeignKey('Departments.DeptID'))
    department = relationship("Department")

class EmployeeDepartment(Base):
    __tablename__ = 'EmployeesDepartment'
    ID = Column(Integer, primary_key=True)
    EmployeeID = Column(Integer)
    Name = Column(String)
    DeptName = Column(String)

engine = create_engine("mssql+pyodbc://@localhost/Company_Database"
                       "?driver=ODBC+Driver+17+for+SQL+Server"
                         "&trusted_connection=yes")
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

results = session.query(Employee).join(Department).all()

for emp in results:
   name_record = EmployeeDepartment(
       EmployeeID=emp.EmployeeID,
       Name=emp.Name,
       DeptName=emp.department.DeptName
   )
   session.add(name_record)
session.commit()

session.close()