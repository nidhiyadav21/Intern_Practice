import pymongo


if __name__ == "__main__":
    print("Welcome to pyMongo")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    print(client)
    db = client['Nidhi']
    collection = db['MySampleCollection']

    #Find any one Document
    # one = collection.find_one({ "Name": "Nidhi" })
    # print(one)

    #Find many document

    #Cursor 
    allDocs = list(collection.find({'Name':'Nidhi'},{'Name':0}))
    print(len(allDocs))
    for item in allDocs:
          print(item)