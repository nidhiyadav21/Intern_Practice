import pymongo
from pymongo.errors import ServerSelectionTimeoutError

try:
  client = pymongo.MongoClient("mongodb://localhost:27017/",serverSelectionTimeoutMS=2000)
  client.server_info()

  db = client["company_db"]
  employees = db["employees"]
  print("Connected to MongoDB successfully.\n")

 #1.Read
  print("\n1. READ: Current Employees:\n")
  all_employees = employees.find()
  # print(all_employees)
  for person in all_employees:
     print(f"{person['Name']} ({person['role']}) | Skills: {person['skills']}")

 #2.Update
  print("\n2. UPDATE: Employee Details:\n")
  employees.update_many(
     {"Name": "Bhumika"},
     {
         "$push": {"skills": "Full Stack developer"},
         "$set": {"role":"Lead full Stack Developer"}
     }
  )
  # print("\n2. UPDATE: Added 'FastAPI' and promoted to Lead.")
  updated_employee = employees.find_one({"Name": "Bhumika"})
  print(f"\n3. VERIFY: New data for Bhumika: {updated_employee['skills']}")


except ServerSelectionTimeoutError:
     print("Connection failed.\n")