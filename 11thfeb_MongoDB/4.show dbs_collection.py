import pymongo


if __name__ == "__main__":
    print("Welcome to pyMongo")
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    print(client)
    allDatabases = client.list_database_names()
    print(allDatabases)
    col = client["Nidhi"]
    print(col.list_collection_names())
