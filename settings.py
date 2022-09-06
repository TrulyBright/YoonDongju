from functools import cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    JWT_SECRET: str
    NCLOUD_ACCESS_KEY: str
    NCLOUD_SECRET_KEY: str
    NCLOUD_SMS_SERVICE_ID: str
    NCLOUD_SMS_SERVICE_PHONE_NUMBER: str
    DB_CONNECTION_STRING: str
    YONSEI_AUTH_FUNCTION_ENDPOINT: str
    YONSEI_AUTH_FUNCTION_CODE: str


@cache
def get_settings():
    return Settings()
