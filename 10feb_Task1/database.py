from sqlalchemy import create_engine #create_engine-manages the connection pool that talks to your sql server
from sqlalchemy.orm import sessionmaker,declarative_base #Sessionmaker - This creates a new session object whenever you need to talk to the database


DATABASE_URL = (
        "mssql+pyodbc://@localhost/EmployeeDB"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
)
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, bind=engine)

Base = declarative_base() #declarative class - This is a "parent" class

# Dependency to get DB session
def get_db():              #This function is a Generator.This ensures every request gets its own fresh database connection.
    db = SessionLocal()    #Opens a new session
    try:
        yield db           #Provides the session to your API function
    finally:
        db.close()
