
from datetime import datetime
from typing import Any, List, Dict, Optional

from database import schemas_collection
from datamodel import SchemaDefinition
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware


# ---- FastAPI app & CORS ----
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _compute_hash_from_doc(doc: Dict[str, Any]) -> str:
    """
    Helper to compute the same SHA-256 hash used by SchemaDefinition
    without instantiating a model (used for quick normalization paths).
    """
    # Import locally to avoid circular imports and to use the same logic
    from datamodel import SchemaDefinition
    return SchemaDefinition._compute_hash(
        doc.get("name"),
        doc.get("version"),
        doc.get("content"),
    )


# ---- Routes ----
@app.get("/schemas", response_model=List[SchemaDefinition])
async def get_all_schemas() -> List[Dict[str, Any]]:
    """
    Retrieve all schemas. Ensures each document has `id` as the content hash
    and a valid `updated_at`. If the stored `id` is missing/mismatched,
    it will be recomputed to keep the collection consistent.
    """
    docs = list(schemas_collection.find())
    normalized: List[Dict[str, Any]] = []
    for d in docs:
        # Compute the correct content hash
        computed_id = _compute_hash_from_doc(d)
        if d.get("id") != computed_id:
            # Heal legacy/mismatched ids
            d["id"] = computed_id
            # Do not modify updated_at during passive normalization
            schemas_collection.update_one({"_id": d["_id"]}, {"$set": {"id": computed_id}})

        # Ensure updated_at exists (server-side default)
        if d.get("updated_at") is None:
            d["updated_at"] = datetime.utcnow()
            schemas_collection.update_one({"_id": d["_id"]}, {"$set": {"updated_at": d["updated_at"]}})

        # Remove internal MongoDB _id from outward JSON
        d.pop("_id", None)
        normalized.append(d)

    return jsonable_encoder(normalized)


@app.post("/schemas", response_model=SchemaDefinition)
async def add_schema(schema: SchemaDefinition) -> Dict[str, Any]:
    """
    Add a new schema. `id` is deterministically computed from {name, version, content}.
    Server sets `updated_at`.
    """
    # Rebuild model explicitly to guarantee id is based on content, not caller-supplied id
    model = SchemaDefinition(
        name=schema.name,
        version=schema.version,
        content=schema.content,
        updated_at=None,
        id="ignored"  # ignored by validator; kept for clarity
    )
    doc = model.dict()
    doc["updated_at"] = datetime.utcnow()

    # Insert as-is (no ObjectId conversions for id)
    schemas_collection.insert_one(doc)

    # Return exactly what we stored
    return jsonable_encoder(doc)


@app.put("/schemas/{id}", response_model=Dict[str, str])
async def update_schema(id: str, update: SchemaDefinition) -> Dict[str, str]:
    """
    Update schema by `id`. Because `id` is a content hash, any change in
    {name, version, content} will produce a new `id`. This endpoint:
      1) Finds the existing document by the current `id`.
      2) Merges provided fields (ignores `None` and any `id` supplied).
      3) Recomputes `id` from merged content.
      4) Replaces the document and returns the (possibly new) `id`.
    """
    if not isinstance(id, str) or not id.strip():
        raise HTTPException(status_code=400, detail="Invalid schema id (must be a non-empty string)")

    existing = schemas_collection.find_one({"id": id})
    if not existing:
        raise HTTPException(status_code=404, detail="Schema not found")

    # Merge non-None fields from the payload (ignore any 'id' from client)
    payload = update.dict()
    merged = {
        "name": payload.get("name", existing.get("name")),
        "version": payload.get("version", existing.get("version")),
        "content": payload.get("content", existing.get("content")),
    }
    # Compute new hash-based id using SchemaDefinition logic
    new_model = SchemaDefinition(**merged, id="ignored", updated_at=None)
    new_id = new_model.id

    # Build final doc to store
    final_doc = {
        "id": new_id,
        "name": merged["name"],
        "version": merged["version"],
        "content": merged["content"],
        "updated_at": datetime.utcnow(),
    }

    # Replace the existing document (matched by the previous id)
    replace_result = schemas_collection.replace_one({"id": id}, final_doc)
    if replace_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Schema not found during update")

    # If id changed, the caller now has to reference the new id
    return {"message": "Schema updated", "id": new_id}


@app.delete("/schemas/{id}", response_model=Dict[str, str])
async def delete_schema(id: str) -> Dict[str, str]:
    """
    Delete schema by `id`.
    """
    if not isinstance(id, str) or not id.strip():
        raise HTTPException(status_code=400, detail="Invalid schema id (must be a non-empty string)")

    result = schemas_collection.delete_one({"id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Schema not found")
    return {"message": "Schema deleted"}
