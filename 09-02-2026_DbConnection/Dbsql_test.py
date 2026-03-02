from sqlalchemy import create_engine,Integer,String,Float,Column
from sqlalchemy.orm import declarative_base,sessionmaker,relationship

engine = create_engine("mssql+pyodbc://@localhost/company_db"
                       "?driver=ODBC+Driver+17+for+SQL+Server"
                         "&trusted_connection=yes")
Base = declarative_base()

class Tasks(Base):
    __tablename__ = 'Tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    status = Column(String(50))


Session = sessionmaker(bind=engine)
session = Session()

try:
    new_task = Tasks(title="New Task from Pycharm",status="Pending")
    session.add(new_task)
    session.commit()
    print("Task added successfully")
except Exception as e:
    print(f"Error: {e}")
finally:
    session.close()