import pymongo


if __name__ == "__main__":
    print("Welcome to pyMongo")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    print(client)
    db = client['Nidhi']
    collection = db['MySampleCollection']

    prev = {"Name": "Nidhi"}
    nextt = {"$set": {"Location": "Mumbai"}}

    #collection.update_one(prev,nextt)

    up = collection.update_many(prev,nextt)

