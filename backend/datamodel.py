
# datamodel.py
import hashlib
import json
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, model_validator

ALLOWED_FIELD_TYPES = {
    "string",
    "integer",
    "number",
    "boolean",
    "date",
    "datetime",
}


def compute_schema_hash(
    name: str | None,
    version: str | None,
    content: dict[str, Any] | None,
) -> str:
    """
    Compute a deterministic SHA-256 hash from the canonical JSON of {name, version, content}.
    """
    payload = {"name": name, "version": version, "content": content}
    canonical = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


class SchemaDefinition(BaseModel):
    id: str = Field(..., description="Unique identifier for the schema (content hash)")
    name: str | None = Field(
        None,
        description="Human-readable name of the schema",
        min_length=3,
    )
    version: str | None = Field(None, description="Version of the schema")
    content: dict[str, Any] | None = Field(
        None, description="The actual schema content as a dictionary"
    )
    updated_at: datetime | None = Field(
        None, description="Timestamp of the last update"
    )

    @model_validator(mode="before")
    def assign_id_from_content(cls, data: Any):
        """
        Pydantic v2: pre-model validator.
        Always (re)compute `id` from the content so it is deterministic and content-addressed.
        Any provided `id` from the caller is ignored to ensure correctness.
        """
        if not isinstance(data, dict):
            return data
        name = data.get("name")
        version = data.get("version")
        content = data.get("content")
        data["id"] = compute_schema_hash(name, version, content)
        return data

    @model_validator(mode="after")
    def validate_content_field_types(self):
        """
        If `content` is provided, ensure it is a flat dict where each value
        is one of the allowed type strings.
        """
        if self.content is None:
            return self

        if not isinstance(self.content, dict):
            raise ValueError("`content` must be a dictionary")

        for k, v in self.content.items():
            if not isinstance(k, str) or not k:
                raise ValueError("All field names in `content` must be non-empty strings")
            if not isinstance(v, str):
                raise ValueError(
                    f"Type for field '{k}' must be a string (one of {sorted(ALLOWED_FIELD_TYPES)})"
                )
            if v not in ALLOWED_FIELD_TYPES:
                raise ValueError(
                    f"Invalid type '{v}' for field '{k}'. Allowed: {sorted(ALLOWED_FIELD_TYPES)}"
                )
        return self

    class Config:
        populate_by_name = True
