from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://user:password@db:27017")

client = MongoClient(MONGO_URL)
db = client.library_db