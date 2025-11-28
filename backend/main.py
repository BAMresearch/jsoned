# backend\main.py
# #################################################################################
# SECTION 001: Basic CRUD operations for version management
# This section demonstrates GET, POST, DELETE, and a custom "show" function.

from fastapi import FastAPI
from backend.datamodel import SchemaDefinition
from typing import List

app = FastAPI(title="Farm Project API")

# In-memory database for teaching purposes
database: List[SchemaDefinition] = []


@app.get("/")
def read_root():
    return {"message": "Welcome to Farm Project API"}


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


# #################################################################################
# SECTION 002: Other HTTP methods (PUT, PATCH)
from backend.model import UpdateSchema

@app.put("/version/{version_id}")
def alter_version(version_id: str, schema: SchemaDefinition):
    """
    PUT: Replace an existing version completely.
    """
    for idx, item in enumerate(database):
        if item.id == version_id:
            database[idx] = schema
            return {"message": "Version replaced", "version": schema}
    return {"error": "Version not found"}

@app.patch("/version/{version_id}")
def update_version(version_id: str, updates: UpdateSchema):
    """
    PATCH: Update specific fields of a version.
    """
    for item in database:
        if item.id == version_id:
            if updates.name:
                item.name = updates.name
            if updates.version:
                item.version = updates.version
            return {"message": "Version updated", "version": item}
    return {"error": "Version not found"}
