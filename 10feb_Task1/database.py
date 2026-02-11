from sqlalchemy import create_engine #create_engine-manages the connection pool that talks to your sql server
from sqlalchemy.orm import sessionmaker,declarative_base #Sessionmaker - This creates a new session object whenever you need to talk to the database


DATABASE_URL = (
        "mssql+pyodbc://@localhost/EmployeeDB"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
)
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base() #declarative class - This is a "parent" class

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
