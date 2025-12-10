
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, root_validator
import hashlib
import json


class SchemaDefinition(BaseModel):
    id: str = Field(..., description="Unique identifier for the schema (content hash)")
    name: Optional[str] = Field(
        None,
        description="Human-readable name of the schema",
        min_length=3,
    )
    version: Optional[str] = Field(None, description="Version of the schema")
    content: Optional[Dict[str, Any]] = Field(
        None, description="The actual schema content as a dictionary"
    )
    updated_at: Optional[datetime] = Field(
        None, description="Timestamp of the last update"
    )

    @staticmethod
    def _compute_hash(name: Optional[str], version: Optional[str], content: Optional[Dict[str, Any]]) -> str:
        """
        Compute a deterministic SHA-256 hash from the canonical JSON of {name, version, content}.
        """
        payload = {"name": name, "version": version, "content": content}
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()

    @root_validator(pre=True)
    def assign_id_from_content(cls, values):
        """
        Always (re)compute `id` from the content so it is deterministic and content-addressed.
        Any provided `id` is ignored to ensure correctness.
        """
        name = values.get("name")
        version = values.get("version")
        content = values.get("content")
        values["id"] = cls._compute_hash(name, version, content)
