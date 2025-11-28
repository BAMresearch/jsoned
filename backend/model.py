#backend\model.py

# model.py
# SECTION 002: Other HTTP methods and example models
# Demonstrates PUT and PATCH for teaching purposes.

from pydantic import BaseModel

class UpdateSchema(BaseModel):
    """
    Represents partial updates for a schema.
    """
    name: str | None = None
    version: str | None = None



