from typing import Annotated, Any

from pydantic import AnyHttpUrl, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf=8",
    )

    PROJECT_NAME: str = "JSONed"
    API_V1_STR: str = "/api/v1"

    MONGO_DATABASE: str = "jsoned_db"
    MONGO_DATABASE_URI: str = "mongodb://localhost:27017"
    COLLECTION: str = "schemas"

    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyHttpUrl] | str, BeforeValidator(parse_cors)
    ] = []


settings = Settings()
