from pydantic import BaseModel
from datetime import datetime



class SchemaDefinition(BaseModel):
    id: str
    name: str
    version: str
    content: dict  # JSON schema
    updated_at: datetime
