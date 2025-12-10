# TODO add login with oauth2
from fastapi import APIRouter

from jsoned.api.api_v1.endpoints import schemas

api_router = APIRouter()
api_router.include_router(schemas.router, prefix="/schemas", tags=["schemas"])
