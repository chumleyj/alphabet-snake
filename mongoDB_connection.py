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



post = {"_id": id, "name": "Erik", "Character": "Blade", "Character Race": "Dragonborn"}
collection.insert_one(post)

print("Working")