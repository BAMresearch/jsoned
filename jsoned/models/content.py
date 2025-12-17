import hashlib
import json
from typing import Any

from pydantic import BaseModel, Field

from jsoned.models.schema_definition import SchemaDefinition


def hash_content(content: dict[str, Any]) -> str:
    """
    Stable hash for JSON-like dicts. Uses canonical JSON representation (sorted keys, no whitespace)
    and SHA-256 hashing.
    """
    canonical = json.dumps(content, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class ContentUpdate(BaseModel):
    content: dict[str, Any] = Field(..., description="New schema content")


class UpdateResponse(BaseModel):
    updated: bool
    schema: SchemaDefinition
    message: str
