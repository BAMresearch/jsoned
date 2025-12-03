# backend\main.py
from datetime import datetime

from bson import ObjectId
from database import schemas_collection
from datamodel import SchemaDefinition
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from model import UpdateSchema

# https://github.com/BAMresearch/jsoned/tree/main/backend

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Get all schemas
@app.get("/schemas")
async def get_all_schemas():
    schemas = list(schemas_collection.find())
    for s in schemas:
        s["_id"] = str(s["_id"])
    return schemas


# Add new schema
@app.post("/schemas")
async def add_schema(schema: SchemaDefinition):
    schema.updated_at = datetime.utcnow()
    result = schemas_collection.insert_one(schema.dict())
    return {"id": str(result.inserted_id)}


# Update schema (PUT)
@app.put("/schemas/{id}")
async def update_schema(id: str, update: UpdateSchema):
    result = schemas_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": {k: v for k, v in update.dict().items() if v is not None}},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Schema not found")
    return {"message": "Schema updated"}


# Delete schema
@app.delete("/schemas/{id}")
async def delete_schema(id: str):
    result = schemas_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Schema not found")
    return {"message": "Schema deleted"}
