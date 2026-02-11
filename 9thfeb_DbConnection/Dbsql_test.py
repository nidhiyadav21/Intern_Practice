from sqlalchemy import create_engine,text
from sqlalchemy.orm import Session
engine = create_engine('sqlite:///STUDENTS_DB.db',echo = True)

conn = engine.connect()
conn.execute(text("CREATE TABLE IF NOT EXISTS people (name str,age int)"))
conn.commit()

session  = Session(engine)
session.execute(text("INSERT INTO people (name,age) VALUES ('Nidhi', 20)"))
session.commit()