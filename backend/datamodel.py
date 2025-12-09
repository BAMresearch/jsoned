from datetime import datetime
from pydantic import BaseModel, Field
from datetime import datetime
from pydantic import BaseModel, Field


class SchemaDefinition(BaseModel):
    id: str = Field(..., description="Unique identifier for the schema")
    name: str | None = Field(
        None ,
        description="Human-readable name of the schema",
        min_length=3,
    )
    version: str | None  = Field(None, description="Version of the schema")
    content: dict | None  = Field(None, description="The actual schema content as a dictionary")
    updated_at: datetime | None = Field(
        None, description="Timestamp of the last update"
    )
