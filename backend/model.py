#backend\model.py
#Defines auxiliary or update models (e.g., UpdateSchema) for partial updates or specialized requests.
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
from pydantic import BaseModel

class UpdateSchema(BaseModel):
    name: str | None = None
    version: str | None = None
