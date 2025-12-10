from typing import Annotated, Any

from pydantic import AnyHttpUrl, BeforeValidator
from pydantic_settings import BaseSettings


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    PROJECT_NAME: str = "JSONed"
    API_V1_STR: str = "/api/v1"
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyHttpUrl] | str, BeforeValidator(parse_cors)
    ] = ["http://localhost", "http://localhost:3000"]


settings = Settings()
