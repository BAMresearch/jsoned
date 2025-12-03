from datetime import datetime
from pydantic import BaseModel, Field

class SchemaDefinition(BaseModel):
    id: str = Field(..., description="Unique identifier for the schema")
    name: str = Field(
        ...,
        description="Human-readable name of the schema",
        min_length=3  # 👈 enforce minimum length
    )
    version: str = Field(
        "1.0.0",
        description="Version of the schema"
    )
    content: dict = Field(
        ...,
        description="The actual schema content as a dictionary"
    )
    updated_at: datetime | None = Field(
        None,
        description="Timestamp of the last update (optional)"
    )
