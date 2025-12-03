
from datetime import datetime

from bson import ObjectId
from database import schemas_collection
from datamodel import SchemaDefinition, UpdateSchema  # ✅ Updated import
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for all origins
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
    Retrieve all schemas from the database.

    Returns:
        list: A list of schema documents with stringified IDs.
    """
    schemas = list(schemas_collection.find())
    for s in schemas:
        s["_id"] = str(s["_id"])
    return schemas

@app.post("/schemas")
async def add_schema(schema: SchemaDefinition):
    """
    Add a new schema to the database.

    Args:
        schema (SchemaDefinition): The schema data to insert.

    Returns:
        dict: The ID of the inserted schema.
    """
    schema.updated_at = datetime.utcnow()
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
    result = schemas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {k: v for k, v in update.dict().items() if v is not None}},
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
    return {"message": "Schema deleted"}
