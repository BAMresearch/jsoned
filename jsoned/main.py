from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from jsoned.api.api_v1.api import api_router
from jsoned.database import close_mongo, connect_to_mongo
from jsoned.settings import settings


@asynccontextmanager
async def app_init(app: FastAPI):
    await connect_to_mongo()

    app.include_router(api_router, prefix=settings.API_V1_STR)
    yield

    await close_mongo()


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=app_init,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(o) for o in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
