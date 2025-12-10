from motor.motor_asyncio import AsyncIOMotorClient

from jsoned.settings import settings

client: AsyncIOMotorClient | None = None
database = None
schemas_collection = None


async def connect_to_mongo():
    global client, database, schemas_collection

    client = AsyncIOMotorClient(settings.MONGO_URI)
    database = client.jsoned_db
    schemas_collection = database.schemas

    # create index once on startup
    await schemas_collection.create_index("title", unique=True)


async def close_mongo():
    if client is not None:
        client.close()
