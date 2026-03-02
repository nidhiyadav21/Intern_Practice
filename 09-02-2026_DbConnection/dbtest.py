# import pyodbc
# import sys
# #from sqlalchemy import create_engine
#
# #engine = create_engine("mssql+pyodbc://localhost/harsh?driver=ODBC+Driver+17+for+SQL+Server")
#
#
# #connect to database
# try:
#     conn = pyodbc.connect("mssql+pyodbc://localhost/STUDENTS_DB?driver=ODBC+Driver+17+for+SQL+Server")
#     print("Connected to DB")
# except Exception as e:
#     print(str(e))
#     sys.exit(0)
#
# query = """ INSERT INTO student_details (FIRSTNAME, LASTNAME, DOB, STANDARD, SECTION) VALUES [?, ?, ?, ?, ?] """, ['Nidhi', 'Yadav', '2005-06-15', 10, 'A']
#
# #execute the query
# try:
#     cursor = conn.cursor()
#     cursor.execute(query)
#     conn.commit()
# except Exception as e:
#     print(str(e))
#     sys.exit(0)
#
#     #close the connection
# conn.close()




import pyodbc
import sys

# Standard pyodbc connection string
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost;"
    "Database=STUDENTS_DB;"
    "Trusted_Connection=yes;"
)

try:
    conn = pyodbc.connect(conn_str)
    print("Connected to DB")
except Exception as e:
    print(f"Connection Error: {e}")
    sys.exit(0)

# 1. Fixed SQL syntax: use () instead of []
sql = "INSERT INTO student_details (FIRSTNAME, LASTNAME, DOB, STANDARD, SECTION) VALUES (?, ?, ?, ?, ?)"
params = [
    ('Nidhi', 'Yadav', 20050615, 10, 'A'),
    ('Bhumika','Chauhan',20050516,11,'B')
    ]

try:
    cursor = conn.cursor()
    # 2. Pass query and params as two separate arguments
    cursor.executemany(sql, params)
    conn.commit()
    print("Record inserted successfully")
except Exception as e:
    print(f"Query Error: {e}")
finally:
    conn.close()
