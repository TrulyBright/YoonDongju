from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str
    yonsei_fetch_api_endpoint: str
    yonsei_fetch_api_yonsei_id: int
    yonsei_login_api_endpoint: str
    yonsei_login_api_function: str
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
