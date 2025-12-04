from datetime import datetime

from bson import ObjectId
from database import schemas_collection
from datamodel import SchemaDefinition, UpdateSchema
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI application
app = FastAPI()

# Enable CORS for all origins (useful for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/schemas")
async def get_all_schemas():
    """
    Retrieve all schema documents from the database.
    Converts MongoDB ObjectId to string for JSON serialization.
    Returns:
        list: A list of schema documents with stringified IDs.
    """
    # Fetch all schema documents from MongoDB
    schema_documents = list(schemas_collection.find())

    # Verbose loop: clarify what we're iterating over and why
    for schema_document in schema_documents:
        # Each schema_document is a MongoDB record representing a schema definition
        # Convert its ObjectId to string so it can be returned in JSON
        original_id = schema_document["_id"]
        schema_document["_id"] = str(original_id)

        # Optional: Add logging or debugging info
        # print(f"Converted ObjectId {original_id} to string for schema: {schema_document}")

    return schema_documents


@app.post("/schemas")
async def add_schema(schema: SchemaDefinition):
    """
    Add a new schema to the database.
    Args:
        schema (SchemaDefinition): The schema data to insert.
    Returns:
        dict: The ID of the inserted schema.
    """
    # Update timestamp before insertion
    schema.updated_at = datetime.utcnow()

    # Insert schema into MongoDB
    result = schemas_collection.insert_one(schema.dict())

    return {"id": str(result.inserted_id)}


@app.put("/schemas/{id}")
async def update_schema(id: str, update: UpdateSchema):
    """
    Update an existing schema by ID.
    Args:
        id (str): The schema ID.
        update (UpdateSchema): Fields to update.
    Raises:
        HTTPException: If the schema is not found.
    Returns:
        dict: Success message.
    """
    # Prepare update fields (ignore None values)
    update_fields = {
        key: value for key, value in update.dict().items() if value is not None
    }

    result = schemas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_fields},
    )

    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Schema not found")

    return {"message": "Schema updated"}


@app.delete("/schemas/{id}")
async def delete_schema(id: str):
    """
    Delete a schema by ID.
    Args:
        id (str): The schema ID.
    Raises:
        HTTPException: If the schema is not found.
    Returns:
        dict: Success message.
    """
    result = schemas_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Schema not found")
