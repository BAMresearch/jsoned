
from datetime import datetime
from typing import Any, Dict, List

from bson import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from database import schemas_collection
from datamodel import SchemaDefinition, UpdateSchema


# ---- FastAPI app & CORS ----
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- Routes ----
@app.get("/schemas")
async def get_all_schemas() -> List[Dict[str, Any]]:
    """
    Retrieve all schema documents from the database.

    Returns:
        list: A list of schema documents with JSON-safe '_id' fields (strings).
    """
    docs = list(schemas_collection.find())
    # One-liner conversion: ObjectId -> str (applies even to nested ObjectIds)
    return jsonable_encoder(docs, custom_encoder={ObjectId: str})


@app.post("/schemas")
async def add_schema(schema: SchemaDefinition) -> Dict[str, Any]:
    """
    Add a new schema to the database.

    Args:
        schema (SchemaDefinition): The schema data to insert.

    Returns:
        dict: A dictionary with keys:
              - "id": the ID of the inserted schema (string),
              - "schema": the actual inserted schema document as stored in the database,
                          with JSON-safe '_id' and other BSON types.
    """
    # Set server-side timestamp
    schema.updated_at = datetime.utcnow()

    # Insert and obtain new ObjectId
    result = schemas_collection.insert_one(schema.dict())
    inserted_oid = result.inserted_id

    # Fetch the stored document to return exactly what's in DB
    inserted_doc = schemas_collection.find_one({"_id": inserted_oid})

    # Make the document JSON-safe (ObjectId -> str, etc.)
    inserted_doc_json = jsonable_encoder(inserted_doc, custom_encoder={ObjectId: str})

    # Stable, tooling-friendly shape:
    return {"id": str(inserted_oid), "schema": inserted_doc_json}

    # If you want ID-as-key instead, return this:
    # return {str(inserted_oid): inserted_doc_json}


@app.put("/schemas/{id}")
async def update_schema(id: str, update: UpdateSchema) -> Dict[str, Any]:
    """
    Update an existing schema by ID.

    Args:
        id (str): The schema ID (string form of ObjectId).
        update (UpdateSchema): Fields to update.

    Raises:
        HTTPException: If the schema is not found.

    Returns:
        dict: Success message and (optionally) the updated document.
    """
    # Prepare update fields (ignore None values)
    update_fields = {k: v for k, v in update.dict().items() if v is not None}

    # If anything is updated, refresh timestamp
    if update_fields:
        update_fields["updated_at"] = datetime.utcnow()

    result = schemas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_fields} if update_fields else {}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Schema not found")

    # Optionally return the updated document (commented out by default)
    # updated_doc = schemas_collection.find_one({"_id": ObjectId(id)})
    # return {
    #     "message": "Schema updated",
    #     "schema": jsonable_encoder(updated_doc, custom_encoder={ObjectId: str}),
    # }

    return {"message": "Schema updated"}


@app.delete("/schemas/{id}")
async def delete_schema(id: str) -> Dict[str, str]:
    """
    Delete a schema by ID.

    Args:
        id (str): The schema ID (string form of ObjectId).

    Raises:
        HTTPException: If the schema is not found.

    Returns:
        dict: Success message.
    """
    result = schemas_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Schema not found")

    return {"message": "Schema deleted"}
