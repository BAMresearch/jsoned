from pydantic import BaseModel


class SchemaDefinition(BaseModel):
    id: str
    name: str
    version: str
    content: dict  # JSON schema
    updated_at: datetime
