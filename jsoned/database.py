# from pymongo import MongoClient

# client = MongoClient("mongodb://localhost:27017/")
# db = client["jsoned_db"]
# schemas_collection = db["schemas"]


from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Driver
client = AsyncIOMotorClient("mongodb://localhost:27017")
database = client.jsoned_db
schemas_collection = database.schemas

# Ensure that the `title` field is unique
schemas_collection.create_index([("title", 1)], unique=True)
