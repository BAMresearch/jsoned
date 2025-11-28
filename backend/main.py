#backend\main.py


# main.py
# SECTION 001: Basic CRUD operations for version management
# This section demonstrates GET, POST, DELETE, and a custom "show" function.

from fastapi import FastAPI
from backend.datamodel import SchemaDefinition
from typing import List

app = FastAPI(title="Farm Project API")

# In-memory database for teaching purposes
database: List[SchemaDefinition] = []

@app.get("/version")
def get_versions():
    """
    GET: Retrieve all versions from the database.
    Returns a list of SchemaDefinition objects.
    """
    return database

@app.post("/version")
def add_version(schema: SchemaDefinition):
    """
    POST: Add a new version to the database.
    Accepts SchemaDefinition as JSON.
    """
    database.append(schema)
    return {"message": "Version added successfully", "version": schema}

@app.delete("/version/{version_id}")
def delete_version(version_id: str):
    """
    DELETE: Remove a version by its ID.
    """
    global database
    database = [item for item in database if item.id != version_id]
    return {"message": f"Version {version_id} deleted"}

@app.get("/version/show")
def show_version_data():
    """
    Custom GET: Show version data in a formatted way.
    Useful for teaching how to return structured data.
    """
    return {"count": len(database), "versions": database}
