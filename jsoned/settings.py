from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "JSONed"
    API_V1_STR: str = "/api/v1"

    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "jsoned_db"
    SCHEMAS_COLLECTION_NAME: str = "schemas"

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:3000",
    ]


settings = Settings()
