from functools import cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    jwt_secret: str
    ncloud_access_key: str
    ncloud_secret_key: str
    ncloud_sms_service_id: str
    ncloud_sms_service_phone_number: str
    db_dialect: str
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_database: str
    yonsei_auth_function_endpoint: str
    yonsei_auth_function_code: str


@cache
def get_settings():
    return Settings()
