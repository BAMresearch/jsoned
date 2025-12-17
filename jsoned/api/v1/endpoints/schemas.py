from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, HTTPException, Request, status
from pymongo.errors import DuplicateKeyError

from jsoned.models.schema_definition import (
    ContentUpdate,
    SchemaCreate,
    SchemaDefinition,
    UpdateResponse,
    hash_content,
)

router = APIRouter()


@router.get("/all", response_model=list[SchemaDefinition])
async def get_all_schemas(request: Request):
    collection = request.app.state.schemas_collection
    docs = collection.find({})
    all_docs = []
    async for doc in docs:
        doc["_id"] = str(doc["_id"])
        all_docs.append(SchemaDefinition(**doc))
    return all_docs


@router.post(
    "/add", response_model=SchemaDefinition, status_code=status.HTTP_201_CREATED
)
async def add_schema(request: Request, payload: SchemaCreate):
    collection = request.app.state.schemas_collection
    now = datetime.now(timezone.utc)

    # Build doc to insert, excluding None fields
    doc = {
        "title": payload.title,
        "content": payload.content,
        "created_at": now,
        "updated_at": now,
        "content_hash": hash_content(payload.content),
    }

    try:
        result = await collection.insert_one(doc)
    except DuplicateKeyError:
        # you created a unique index on title
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A schema with this title already exists.",
        )
    doc["_id"] = str(result.inserted_id)
    return SchemaDefinition(**doc)


@router.delete("/delete/{title}", status_code=status.HTTP_200_OK)
async def delete_schema_by_title(
    request: Request,
    title: str,
):
    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide exactly one of: id or title",
        )

    collection = request.app.state.schemas_collection
    result = await collection.delete_one({"title": title})
    if result.deleted_count == 0:
        raise HTTPException(404, f"Schema with title `{title}` not found")

    return {"message": "Schema deleted"}


@router.delete("/delete/id/{id}", status_code=status.HTTP_200_OK)
async def delete_schema_by_id(
    request: Request,
    id: str,
):
    collection = request.app.state.schemas_collection
    try:
        oid = ObjectId(id)
    except InvalidId:
        raise HTTPException(400, "Invalid Mongo ObjectId")

    result = await collection.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(404, f"Schema with id `{id}` not found")

    return {"message": "Schema deleted"}


@router.put(
    "/update/content/{id}",
    response_model=UpdateResponse,
    status_code=status.HTTP_200_OK,
)
async def update_schema_by_id(
    request: Request,
    id: str,
    update: ContentUpdate,
):
    collection = request.app.state.schemas_collection
    try:
        oid = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid Mongo ObjectId")

    # Fetch current doc and hash
    current = await collection.find_one({"_id": oid})
    if current is None:
        raise HTTPException(status_code=404, detail=f"Schema with id `{id}` not found")

    # hashes
    old_hash = current.get("content_hash")
    new_hash = hash_content(update.content)

    # No change → skip update; return existing doc + message
    if old_hash == new_hash:
        current["_id"] = str(current["_id"])
        return UpdateResponse(
            updated=False,
            schema=SchemaDefinition(**current),
            message="Content unchanged; update skipped.",
        )

    # Content changed → perform update
    updated = await collection.find_one_and_update(
        {"_id": oid},
        {
            "$set": {
                "content": update.content,
                "content_hash": new_hash,
                "updated_at": datetime.now(timezone.utc),
            }
        },
        return_document=True,
    )
    return UpdateResponse(
        updated=True,
        schema=SchemaDefinition(**updated),
        message="Schema updated.",
    )
