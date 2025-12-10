from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request, status
from pymongo.errors import DuplicateKeyError

from jsoned.models.schema_definition import SchemaDefinition

router = APIRouter()


@router.get("/all", response_model=list[SchemaDefinition])
async def get_all_schemas(request: Request):
    schemas_collection = request.app.state.schemas_collection
    docs = schemas_collection.find({})
    return [SchemaDefinition(**doc) async for doc in docs]


@router.post(
    "/add", response_model=SchemaDefinition, status_code=status.HTTP_201_CREATED
)
async def add_schema(request: Request, schema: SchemaDefinition):
    """
    Add a new schema. Requires `content` to be non-null. `updated_at` is always set by the server.
    """
    if schema.content is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="`content` must not be null.",
        )

    schemas_collection = request.app.state.schemas_collection

    # Build doc to insert, excluding None fields
    doc = schema.model_dump(exclude_none=True)
    doc["created_at"] = datetime.now(timezone.utc)

    try:
        await schemas_collection.insert_one(doc)
    except DuplicateKeyError:
        # you created a unique index on title
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A schema with this title already exists.",
        )

    return SchemaDefinition(**doc)


# @router.post("/add", response_model=SchemaDefinition)
# async def add_schema(schema: SchemaDefinition) -> dict[str, Any]:
#     """
#     Add a new schema. If `id` is missing/empty, generate one; always refresh `updated_at`.
#     """
#     doc = schema.dict()

#     # Guarantee a usable id
#     if not isinstance(doc.get("id"), str) or not doc["id"].strip():
#         doc["id"] = str(uuid4())

#     # Server-side timestamp
#     doc["updated_at"] = datetime.utcnow()

#     # Insert as-is (no ObjectId conversions)
#     schemas_collection.insert_one(doc)

#     # Return exactly what we stored
#     return jsonable_encoder(doc)


# @router.put("/update/{id}", response_model=dict[str, str])
# async def update_schema(id: str, update: SchemaDefinition) -> dict[str, str]:
#     """
#     Update schema by `id`. Ignores `id` field in the payload (primary key is immutable).
#     Only non-None fields are updated; `updated_at` is refreshed automatically.
#     """
#     if not isinstance(id, str) or not id.strip():
#         raise HTTPException(
#             status_code=400, detail="Invalid schema id (must be a non-empty string)"
#         )

#     # Ignore None values and prevent changing the primary key
#     update_fields = {
#         k: v for k, v in update.dict().items() if v is not None and k != "id"
#     }

#     if update_fields:
#         update_fields["updated_at"] = datetime.utcnow()

#     result = schemas_collection.update_one(
#         {"id": id}, {"$set": update_fields} if update_fields else {}
#     )
#     if result.matched_count == 0:
#         raise HTTPException(status_code=404, detail="Schema not found")

#     return {"message": "Schema updated"}


# @router.delete("/delete/{id}", response_model=dict[str, str])
# async def delete_schema(id: str) -> dict[str, str]:
#     """
#     Delete schema by `id`.
#     """
#     if not isinstance(id, str) or not id.strip():
#         raise HTTPException(
#             status_code=400, detail="Invalid schema id (must be a non-empty string)"
#         )

#     result = schemas_collection.delete_one({"id": id})
#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Schema not found")

#     return {"message": "Schema deleted"}
