from random import randint
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Database connect
MONGO = os.getenv("MONGO")
cluster = MongoClient(f"{MONGO}")
db = cluster["snake"]
collection = db["snake"]



#post = {"_id": 4, "hardWords": ["Airplane", "Basketball", "Baseball", "Football", "Headlights", "Vacuum", "Mountain", "Receipt"]}
#collection.insert_one(post)

viewDB = collection.find({})
print("Currently in MongoDB.")
for x in viewDB:
    print(x)
    print()


print("Working")