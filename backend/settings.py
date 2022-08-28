from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str
    ncloud_access_key: str
    ncloud_secret_key: str
    ncloud_sms_service_id: str
    ncloud_sms_service_phone_number: str

    class Config:
        env_file = "prod.env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()
