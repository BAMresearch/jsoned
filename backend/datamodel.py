# backend\datamodel.py
# datamodel.py → Defines core data structures (e.g., SchemaDefinition) that represent your main entities.
from datetime import datetime

from pydantic import BaseModel


class SchemaDefinition(BaseModel):
    id: str
    name: str
    version: str
    content: dict
    updated_at: datetime | None = None
