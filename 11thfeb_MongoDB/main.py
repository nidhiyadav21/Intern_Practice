import pymongo
from pymongo.errors import ServerSelectionTimeoutError


def setup_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/",serverSelectionTimeoutMS=2000)

    try:
        client.server_info()
        print("Connection Successful: MongoDB server is running")


        db = client["company_db"]
        employees = db["employees"]

        new_employee = [{
              "Name": "Nidhi",
              "role": "AI Intern",
              "skills": ["python", "django", "pymongo"],
              "experience_years":5
        },{
            "Name": "Bhumika",
            "role": "Backend Intern",
            "skills": ["python", "django", "pymongo"],
            "experience_years": 3

        }
        ]

        employees.insert_many(new_employee)

    except ServerSelectionTimeoutError:
        print("Connection Error")

if __name__ == "__main__":
    setup_mongodb()