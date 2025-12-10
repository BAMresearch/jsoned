from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SchemaDefinition(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str | None = Field(None, alias="_id")

    title: str | None = Field(
        None,
        description="A human-readable title given to the schema entry.",
        min_length=3,
    )

    created_at: datetime | None = Field(
        None,
        description="Timestamp of the creation of the schema entry.",
    )

    updated_at: datetime | None = Field(
        None,
        description="Timestamp of the last update of the schema entry.",
    )

    content: dict | None = Field(
        None,
        description="The actual schema content as a dictionary",
    )
