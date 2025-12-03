from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["jsoned_db"]
schemas_collection = db["schemas"]
