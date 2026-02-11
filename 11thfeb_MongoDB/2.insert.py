import pymongo


if __name__ == "__main__":
    print("Welcome to pyMongo")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    print(client)
    db = client['Nidhi']
    collection = db['MySampleCollection']

    #InsertOne
    # dictionary = {'name': 'Nidhi','marks':80}
    # collection.insert_one(dictionary)

    #InsertMany
    insertThese = {'_id':7,"Name": "Nidhi","Location": "Chennai", "Marks": 24}
    collection.insert_one(insertThese)