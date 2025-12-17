from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from jsoned.settings import settings

client: AsyncIOMotorClient | None = None
database = None
_schemas_collection: AsyncIOMotorCollection | None = None


async def connect_to_mongo():
    global client, database, _schemas_collection

    client = AsyncIOMotorClient(settings.MONGO_DATABASE_URI)
    database = client[settings.MONGO_DATABASE]
    _schemas_collection = database[settings.COLLECTION]

    await _schemas_collection.create_index("title", unique=True)


async def close_mongo():
    if client is not None:
        client.close()


def get_schemas_collection() -> AsyncIOMotorCollection:
    if _schemas_collection is None:
        raise HTTPException(503, "Database not available")
    return _schemas_collection
