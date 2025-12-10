from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "JSONed"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = [
        "http://localhost",
        "http://localhost:3000",
    ]
    MONGO_URI: AnyHttpUrl = "mongodb://localhost:27017"


settings = Settings()
