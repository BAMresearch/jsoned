
# main.py
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from database import schemas_collection
from datamodel import SchemaDefinition, compute_schema_hash, ALLOWED_FIELD_TYPES

# ---- FastAPI app & CORS ----
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Helpers ----
def _merge_flat_content(existing: Optional[Dict[str, Any]], incoming: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Merge two flat dicts for schema `content`.
    - Existing values are overwritten by incoming values for the same key.
    - New keys in incoming are added.
    """
    base = dict(existing or {})
    if incoming:
        for k, v in incoming.items():
            base[k] = v
    return base


# ---- Routes ----
@app.get("/schemas", response_model=list[SchemaDefinition])
async def get_all_schemas() -> list[dict[str, Any]]:
    """
    Retrieve all schemas. Ensures each document has `id` as the content hash
    and a valid `updated_at`. If the stored `id` is missing/mismatched,
    it will be recomputed to keep the collection consistent.
    """
    docs = list(schemas_collection.find())
    normalized: list[dict[str, Any]] = []
    for d in docs:
        computed_id = compute_schema_hash(
            d.get("name"), d.get("version"), d.get("content")
        )
        if d.get("id") != computed_id:
            d["id"] = computed_id
            schemas_collection.update_one(
                {"_id": d["_id"]}, {"$set": {"id": computed_id}}
            )
        if d.get("updated_at") is None:
            d["updated_at"] = datetime.utcnow()
            schemas_collection.update_one(
                {"_id": d["_id"]}, {"$set": {"updated_at": d["updated_at"]}}
            )
        d.pop("_id", None)
        normalized.append(d)
    return jsonable_encoder(normalized)


@app.post("/schemas", response_model=SchemaDefinition)
async def add_schema(schema: SchemaDefinition) -> dict[str, Any]:
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
        id="ignored",  # ignored by model_validator
    )
    doc = model.dict()
    doc["updated_at"] = datetime.utcnow()
    schemas_collection.insert_one(doc)
    return jsonable_encoder(doc)


@app.put("/schemas/{id}", response_model=dict[str, str])
async def update_schema(id: str, update: SchemaDefinition) -> dict[str, str]:
    """
    Update schema by `id`.

    Behavior:
    - Finds existing document by current `id`.
    - Merges provided fields (ignores any None and any `id` supplied).
    - `content` is MERGED: existing fields preserved unless explicitly changed; new fields added.
    - Recomputes `id` from merged content and replaces the document.

    Notes:
    - Because `id` is a hash of {name, version, content}, any change can produce a new `id`.
    """
    if not isinstance(id, str) or not id.strip():
        raise HTTPException(
            status_code=400, detail="Invalid schema id (must be a non-empty string)"
        )

    existing = schemas_collection.find_one({"id": id})
    if not existing:
        raise HTTPException(status_code=404, detail="Schema not found")

    payload = update.dict()

    merged_name = payload.get("name") if payload.get("name") is not None else existing.get("name")
    merged_version = payload.get("version") if payload.get("version") is not None else existing.get("version")

    # --- Merge content (flat dict) ---
    incoming_content = payload.get("content")
    merged_content = _merge_flat_content(existing.get("content"), incoming_content)

    # Optional: validate merged content types
    for k, v in merged_content.items():
        if not isinstance(v, str) or v not in ALLOWED_FIELD_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid type for field '{k}': '{v}'. Allowed: {sorted(ALLOWED_FIELD_TYPES)}",
            )

    new_id = compute_schema_hash(merged_name, merged_version, merged_content)

    final_doc = {
        "id": new_id,
        "name": merged_name,
        "version": merged_version,
        "content": merged_content,
        "updated_at": datetime.utcnow(),
    }

    replace_result = schemas_collection.replace_one({"id": id}, final_doc)
    if replace_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Schema not found during update")

    return {"message": "Schema updated", "id": new_id}


@app.patch("/schemas/{id}/content", response_model=dict[str, str])
async def patch_schema_content(id: str, content_updates: Dict[str, str]) -> dict[str, str]:
    """
    Convenience endpoint to ONLY upsert fields in `content`:
    - Adds new fields.
    - Changes type of existing fields.
    - Does not touch `name` or `version`.

    Example body:
    {
      "age": "integer",
      "email": "string"
    }
    """
    if not isinstance(id, str) or not id.strip():
        raise HTTPException(
            status_code=400, detail="Invalid schema id (must be a non-empty string)"
        )

    existing = schemas_collection.find_one({"id": id})
    if not existing:
        raise HTTPException(status_code=404, detail="Schema not found")

    # Validate incoming updates
    if not isinstance(content_updates, dict):
        raise HTTPException(status_code=400, detail="Body must be a JSON object")

    for k, v in content_updates.items():
        if not isinstance(k, str) or not k.strip():
            raise HTTPException(status_code=400, detail="Field names must be non-empty strings")
        if not isinstance(v, str) or v not in ALLOWED_FIELD_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid type for field '{k}': '{v}'. Allowed: {sorted(ALLOWED_FIELD_TYPES)}",
            )

    merged_content = _merge_flat_content(existing.get("content"), content_updates)

    new_id = compute_schema_hash(existing.get("name"), existing.get("version"), merged_content)

    final_doc = {
        "id": new_id,
        "name": existing.get("name"),
        "version": existing.get("version"),
        "content": merged_content,
        "updated_at": datetime.utcnow(),
    }

    replace_result = schemas_collection.replace_one({"id": id}, final_doc)
    if replace_result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Schema not found during update")

    return {"message": "Content patched", "id": new_id}


@app.delete("/schemas/{id}", response_model=dict[str, str])
async def delete_schema(id: str) -> dict[str, str]:
    """
    Delete schema by `id`.
    """
    if not isinstance(id, str) or not id.strip():
        raise HTTPException(
            status_code=400, detail="Invalid schema id (must be a non-empty string)"
        )
    result = schemas_collection.delete_one({"id": id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Schema not found")
    return {"message": "Schema deleted"}
