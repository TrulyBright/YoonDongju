from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str
    ncloud_access_key: str
    ncloud_secret_key: str
    ncloud_archive_storage_domain_id: str
    ncloud_archive_storage_project_id: str

    class Config:
        env_file = "prod.env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()
