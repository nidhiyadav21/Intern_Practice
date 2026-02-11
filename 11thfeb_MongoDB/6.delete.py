import pymongo


if __name__ == "__main__":
    print("Welcome to pyMongo")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    print(client)
    db = client['Nidhi']
    collection = db['MySampleCollection']

    rec = {"Name": "Nidhi"}

    # collection.delete_one(rec)

    up = collection.delete_many(rec)

