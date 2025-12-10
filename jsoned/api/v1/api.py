from fastapi import APIRouter

from jsoned.api.v1.endpoints import schemas

api_router = APIRouter()
api_router.include_router(schemas.router, prefix="/schemas", tags=["schemas"])
# TODO add login with oauth2
# api_router.include_router(login.router, prefix="/login", tags=["login"])
