from functools import lru_cache
from pydantic import BaseSettings
from fastapi_jwt_auth import AuthJWT


class Settings(BaseSettings):
    jwt_secret: str
    authjwt_secret_key: str

    class Config:
        env_file = "prod.env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()
