import hashlib
import json
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


def hash_content(content: dict[str, Any]) -> str:
    """
    Stable hash for JSON-like dicts. Uses canonical JSON representation (sorted keys, no whitespace)
    and SHA-256 hashing.
    """
    canonical = json.dumps(content, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class SchemaCreate(BaseModel):
    title: str = Field(
        ...,
        description="A human-readable title given to the schema entry.",
        min_length=3,
    )
    content: dict | None = Field(
        None,
        description="The actual schema content as a dictionary",
    )


class SchemaDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str | None = Field(None, alias="_id")

    title: str | None = Field(
        None,
        description="A human-readable title given to the schema entry.",
        min_length=3,
    )
    content: dict | None = Field(
        None,
        description="The actual schema content as a dictionary",
    )

    created_at: datetime | None = Field(
        None,
        description="Timestamp of the creation of the schema entry.",
    )

    updated_at: datetime | None = Field(
        None,
        description="Timestamp of the last update of the schema entry.",
    )

    content_hash: str | None = Field(
        None,
        description="A stable hash of the schema content for integrity verification",
    )


class ContentUpdate(BaseModel):
    content: dict[str, Any] = Field(..., description="New schema content")


class UpdateResponse(BaseModel):
    updated: bool
    schema: SchemaDefinition
    message: str
