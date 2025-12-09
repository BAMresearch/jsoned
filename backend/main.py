
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from database import schemas_collection
from datamodel import SchemaDefinition

# ---- FastAPI app & CORS ----
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Routes ----
@app.get("/schemas", response_model=List[SchemaDefinition])
async def get_all_schemas() -> List[Dict[str, Any]]:
    """
    Retrieve all schemas. Each schema uses `id` as a string.
    """
    docs = list(schemas_collection.find())
    # Ensure all docs have `id` as string
    normalized = []
    for d in docs:
        if "id" not in d or not isinstance(d["id"], str):
            d["id"] = str(d.get("id", uuid4()))
        normalized.append(d)
    return jsonable_encoder(normalized)


@app.post("/schemas", response_model=SchemaDefinition)
async def add_schema(schema: SchemaDefinition) -> Dict[str, Any]:
    """
    Add a new schema. If `id` is missing, generate one.
    """
    doc = schema.dict()
    # Ensure `id` exists
    if not doc.get("id"):
        doc["id"] = str(uuid4())
    # Set updated_at
    doc["updated_at"] = datetime.utcnow()
    # Insert into MongoDB
    schemas_collection.insert_one(doc)
    return jsonable_encoder(doc)


@app.put("/schemas/{id}", response_model=Dict[str, str])
async def update_schema(id: str, update: SchemaDefinition) -> Dict[str, str]:
    """
    Update schema by `id`. Ignore None values except updated_at.
    """
    update_fields = {k: v for k, v in update.dict().items() if v is not None and k != "id"}
    if update_fields:
        update_fields["updated_at"] = datetime.utcnow()
    result = schemas_collection.update_one({"id": id}, {"$set": update_fields} if update_fields else {})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Schema not found")
    return {"message": "Schema updated"}


@app.delete("/schemas/{id}", response_model=Dict[str, str])
async def delete_schema(id: str) -> Dict[str, str]:
    """
    Delete schema by `id`.
    """
    result = schemas_collection.delete_one({"id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Schema not found")
    return {"message": "Schema deleted"}
