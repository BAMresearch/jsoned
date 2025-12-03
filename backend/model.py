# Defines auxiliary or update models (e.g., UpdateSchema) for partial updates or specialized requests.
"""### ✅ Best Practice for Large Projects - A common structure for FastAPI projects:

backend/
├── main.py
├── database.py
├── models/          # Folder for all models
│   ├── datamodel.py # Core entities
│   ├── update.py    # Update/patch models
│   ├── user.py      # User-related models
│   └── ...
├── routers/         # API routes
├── services/        # Business logic
├── utils/           # Helpers
"""

from datetime import datetime

from pydantic import BaseModel, Field


class SchemaDefinition(BaseModel):
    id: str = Field(..., description="Unique identifier for the schema")
    name: str = Field(
        ..., description="Human-readable name of the schema", min_length=3
    )
    version: str = Field("1.0.0", description="Version of the schema")
    content: dict = Field(..., description="The actual schema content as a dictionary")
    updated_at: datetime | None = Field(
        None, description="Timestamp of the last update (optional)"
    )


class UpdateSchema(BaseModel):
    name: str | None = None
    version: str | None = None
