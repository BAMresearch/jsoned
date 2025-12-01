#backend\datamodel.py
#datamodel.py → Defines core data structures (e.g., SchemaDefinition) that represent your main entities.
from pydantic import BaseModel
from datetime import datetime

class SchemaDefinition(BaseModel):
    id: str
    name: str
    version: str
    content: dict
    updated_at: datetime | None = None
